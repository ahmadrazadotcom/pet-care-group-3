import os
import secrets
from functools import wraps
from pathlib import Path
from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
from core import (CARE_TYPES, connect, init_db, register_user, authenticate, owned_pet,
                  save_pet, add_care, add_appointment, reminders)


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32),
                      DATABASE=os.environ.get('DATABASE_PATH', str(Path(app.instance_path)/'petcare.sqlite3')),
                      SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',
                      SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE')=='1', MAX_CONTENT_LENGTH=64*1024)
    if config: app.config.update(config)
    Path(app.config['DATABASE']).parent.mkdir(parents=True, exist_ok=True)
    db = connect(app.config['DATABASE']); init_db(db); db.close()

    def database():
        if 'db' not in g: g.db = connect(app.config['DATABASE'])
        return g.db

    @app.teardown_appcontext
    def close_db(error=None):
        db = g.pop('db',None)
        if db: db.close()

    @app.context_processor
    def csrf_context():
        if 'csrf' not in session: session['csrf'] = secrets.token_hex(24)
        return {'csrf_token':session['csrf']}

    @app.before_request
    def check_csrf():
        if request.method == 'POST':
            token = session.get('csrf','')
            if not token or not secrets.compare_digest(token,request.form.get('csrf_token','')): abort(400)

    def login_required(view):
        @wraps(view)
        def wrapped(*args,**kwargs):
            if 'user_id' not in session: return redirect(url_for('login'))
            return view(*args,**kwargs)
        return wrapped

    def pet_or_404(pet_id):
        pet = owned_pet(database(),session['user_id'],pet_id)
        if not pet: abort(404)
        return pet

    @app.route('/')
    @login_required
    def dashboard():
        owner = session['user_id']
        pets = database().execute('SELECT * FROM pets WHERE owner_id=? ORDER BY name',(owner,)).fetchall()
        return render_template('dashboard.html',pets=pets,reminders=reminders(database(),owner))

    @app.route('/register',methods=['GET','POST'])
    def register():
        if request.method=='POST':
            try:
                register_user(database(),request.form.get('email',''),request.form.get('password',''))
            except ValueError as err: flash(str(err),'error')
            else:
                flash('Account created. You can now sign in.','success')
                return redirect(url_for('login'))
        return render_template('auth.html',register=True)

    @app.route('/login',methods=['GET','POST'])
    def login():
        if request.method=='POST':
            user = authenticate(database(),request.form.get('email',''),request.form.get('password',''))
            if user:
                session.clear(); session['user_id']=user
                return redirect(url_for('dashboard'))
            flash('Email or password is incorrect.','error')
        return render_template('auth.html',register=False)

    @app.post('/logout')
    @login_required
    def logout():
        session.clear(); return redirect(url_for('login'))

    @app.route('/pets/new',methods=['GET','POST'])
    @app.route('/pets/<int:pet_id>/edit',methods=['GET','POST'])
    @login_required
    def pet_form(pet_id=None):
        pet = pet_or_404(pet_id) if pet_id is not None else None
        if request.method=='POST':
            try:
                saved = save_pet(database(),session['user_id'],request.form.get('name',''),request.form.get('species',''),request.form.get('breed',''),pet_id)
            except ValueError as err: flash(str(err),'error')
            else:
                flash('Pet details saved.','success'); return redirect(url_for('pet_detail',pet_id=saved))
        return render_template('pet_form.html',pet=pet)

    @app.get('/pets/<int:pet_id>')
    @login_required
    def pet_detail(pet_id):
        pet = pet_or_404(pet_id)
        care = database().execute('SELECT * FROM care WHERE pet_id=? ORDER BY care_date DESC,id DESC',(pet_id,)).fetchall()
        appointments = database().execute('SELECT * FROM appointments WHERE pet_id=? ORDER BY visit_at',(pet_id,)).fetchall()
        return render_template('pet.html',pet=pet,care=care,appointments=appointments)

    @app.route('/pets/<int:pet_id>/care/new',methods=['GET','POST'])
    @login_required
    def care_form(pet_id):
        pet = pet_or_404(pet_id)
        if request.method=='POST':
            try: add_care(database(),session['user_id'],pet_id,request.form.get('kind',''),request.form.get('care_date',''),request.form.get('notes',''),request.form.get('due_date',''))
            except ValueError as err: flash(str(err),'error')
            else: flash('Care record saved.','success'); return redirect(url_for('pet_detail',pet_id=pet_id))
        return render_template('record.html',pet=pet,is_care=True,types=CARE_TYPES)

    @app.route('/pets/<int:pet_id>/appointments/new',methods=['GET','POST'])
    @login_required
    def appointment_form(pet_id):
        pet = pet_or_404(pet_id)
        if request.method=='POST':
            try: add_appointment(database(),session['user_id'],pet_id,request.form.get('clinic',''),request.form.get('visit_at',''),request.form.get('notes',''))
            except ValueError as err: flash(str(err),'error')
            else: flash('Appointment saved.','success'); return redirect(url_for('pet_detail',pet_id=pet_id))
        return render_template('record.html',pet=pet,is_care=False)
    return app

app = create_app()

if __name__=='__main__':
    app.run(port=5000)
