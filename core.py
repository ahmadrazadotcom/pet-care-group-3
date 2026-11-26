"""Database and date rules for the Pet Care Information System."""
import sqlite3
import hashlib
import hmac
import secrets
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

CARE_TYPES = ('Vaccination', 'Medication', 'Allergy', 'Treatment')

def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db

def init_db(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS pets (id INTEGER PRIMARY KEY, owner_id INTEGER NOT NULL REFERENCES users(id), name TEXT NOT NULL, species TEXT NOT NULL, breed TEXT NOT NULL DEFAULT '');
    CREATE TABLE IF NOT EXISTS care (id INTEGER PRIMARY KEY, pet_id INTEGER NOT NULL REFERENCES pets(id), kind TEXT NOT NULL, care_date TEXT NOT NULL, notes TEXT NOT NULL, due_date TEXT);
    CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY, pet_id INTEGER NOT NULL REFERENCES pets(id), clinic TEXT NOT NULL, visit_at TEXT NOT NULL, notes TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'active');
    ''')
    db.commit()

def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 600000).hex()
    return salt + ':' + digest

def check_password(password, stored):
    salt, digest = stored.split(':', 1)
    actual = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 600000).hex()
    return hmac.compare_digest(actual, digest)

def valid_email(email):
    import re
    return bool(re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email)) and len(email) <= 254

def register_user(db, email, password):
    email = email.strip().lower()
    if not valid_email(email) or not 8 <= len(password) <= 128:
        raise ValueError('Enter a valid email and a password with 8 to 128 characters.')
    try:
        db.execute('INSERT INTO users(email,password_hash) VALUES (?,?)', (email,hash_password(password)))
        db.commit()
    except sqlite3.IntegrityError:
        raise ValueError('This email is already registered.') from None

def authenticate(db, email, password):
    user = db.execute('SELECT * FROM users WHERE email=?',(email.strip().lower(),)).fetchone()
    return user['id'] if user and len(password) <= 128 and check_password(password,user['password_hash']) else None

def owned_pet(db, owner, pet_id):
    return db.execute('SELECT * FROM pets WHERE id=? AND owner_id=?',(pet_id,owner)).fetchone()

def save_pet(db, owner, name, species, breed='', pet_id=None):
    name, species, breed = name.strip(), species.strip(), breed.strip()
    if not name or not species or max(map(len,(name,species,breed))) > 100:
        raise ValueError('Enter a pet name and species (up to 100 characters).')
    if pet_id is None:
        pet_id = db.execute('INSERT INTO pets(owner_id,name,species,breed) VALUES (?,?,?,?)',(owner,name,species,breed)).lastrowid
    else:
        if not owned_pet(db,owner,pet_id): raise PermissionError('Pet not found.')
        db.execute('UPDATE pets SET name=?,species=?,breed=? WHERE id=? AND owner_id=?',(name,species,breed,pet_id,owner))
    db.commit()
    return pet_id

def parse_date(value):
    try:
        parsed = date.fromisoformat(value)
        if parsed.isoformat() != value: raise ValueError
        return parsed
    except (ValueError, TypeError):
        raise ValueError('Enter a valid date.') from None

def add_care(db, owner, pet_id, kind, care_date, notes='', due_date=''):
    if not owned_pet(db,owner,pet_id): raise PermissionError('Pet not found.')
    if kind not in CARE_TYPES: raise ValueError('Choose a care type.')
    parse_date(care_date)
    if due_date and parse_date(due_date) < parse_date(care_date):
        raise ValueError('The next due date must not be before the care date.')
    if len(notes) > 1000: raise ValueError('Notes must be 1,000 characters or less.')
    db.execute('INSERT INTO care(pet_id,kind,care_date,notes,due_date) VALUES (?,?,?,?,?)',(pet_id,kind,care_date,notes.strip(),due_date or None))
    db.commit()

def add_appointment(db, owner, pet_id, clinic, visit_at, notes=''):
    if not owned_pet(db,owner,pet_id): raise PermissionError('Pet not found.')
    clinic = clinic.strip()
    if not clinic or len(clinic)>150: raise ValueError('Enter a clinic name (up to 150 characters).')
    try:
        dt = datetime.strptime(visit_at,'%Y-%m-%dT%H:%M')
    except (ValueError,TypeError): raise ValueError('Enter a valid appointment date and time.') from None
    if len(notes)>1000: raise ValueError('Notes must be 1,000 characters or less.')
    db.execute('INSERT INTO appointments(pet_id,clinic,visit_at,notes) VALUES (?,?,?,?)',(pet_id,clinic,dt.isoformat(timespec='minutes'),notes.strip()))
    db.commit()

def reminder_status(value, today):
    day = parse_date(value[:10])
    if day < today: return 'Overdue'
    if day <= today + timedelta(days=7): return 'Upcoming'
    return None

def reminders(db, owner, today=None):
    today = today or datetime.now(ZoneInfo('Australia/Sydney')).date()
    rows = db.execute('''SELECT p.name AS pet, c.kind AS title, c.due_date AS due FROM care c JOIN pets p ON c.pet_id=p.id WHERE p.owner_id=? AND c.due_date IS NOT NULL
        UNION ALL SELECT p.name, a.clinic, a.visit_at FROM appointments a JOIN pets p ON a.pet_id=p.id WHERE p.owner_id=? AND a.status='active' ORDER BY due''',(owner,owner)).fetchall()
    return [dict(row, status=status) for row in rows if (status:=reminder_status(row['due'],today))]
