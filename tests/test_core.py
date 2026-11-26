from datetime import date, timedelta
import pytest
from core import *

@pytest.fixture
def db(tmp_path):
    conn=connect(tmp_path/'test.sqlite3'); init_db(conn)
    register_user(conn,'owner@example.com','Password123')
    register_user(conn,'other@example.com','Password123')
    yield conn
    conn.close()

def test_us01_password_hash(db):
    row=db.execute('SELECT * FROM users WHERE id=1').fetchone()
    assert row['password_hash']!='Password123'
    assert check_password('Password123',row['password_hash'])

def test_us01_duplicate(db):
    with pytest.raises(ValueError,match='already registered'): register_user(db,'OWNER@example.com','Password123')

@pytest.mark.parametrize('email,password',[('wrong','Password123'),('new@example.com','short')])
def test_us01_invalid(db,email,password):
    with pytest.raises(ValueError): register_user(db,email,password)

def test_us02_auth(db):
    assert authenticate(db,'owner@example.com','Password123')==1
    assert authenticate(db,'owner@example.com','wrong') is None
    assert authenticate(db,'missing@example.com','Password123') is None

def test_us03_create_and_isolate(db):
    pet=save_pet(db,1,'Milo','Dog','Labrador')
    assert owned_pet(db,1,pet)['name']=='Milo'
    assert owned_pet(db,2,pet) is None

def test_us04_edit(db):
    pet=save_pet(db,1,'Milo','Dog')
    save_pet(db,1,'Max','Dog','Labrador',pet)
    assert owned_pet(db,1,pet)['name']=='Max'
    with pytest.raises(ValueError): save_pet(db,1,' ','Dog',pet_id=pet)
    with pytest.raises(PermissionError): save_pet(db,2,'Other','Cat',pet_id=pet)

@pytest.mark.parametrize('kind',CARE_TYPES)
def test_us05_care(db,kind):
    pet=save_pet(db,1,'Milo','Dog')
    add_care(db,1,pet,kind,'2026-11-20','Example note','2026-11-25')
    assert db.execute('SELECT kind FROM care').fetchone()['kind']==kind

def test_us05_invalid_care(db):
    pet=save_pet(db,1,'Milo','Dog')
    with pytest.raises(ValueError): add_care(db,1,pet,'Vaccination','2026-02-30')
    with pytest.raises(ValueError): add_care(db,1,pet,'Vaccination','2026-11-20',due_date='2026-11-19')
    with pytest.raises(PermissionError): add_care(db,2,pet,'Vaccination','2026-11-20')

def test_us07_appointment(db):
    pet=save_pet(db,1,'Milo','Dog')
    add_appointment(db,1,pet,'Sample Vet','2026-11-26T10:30')
    assert db.execute('SELECT clinic,visit_at FROM appointments').fetchone()['visit_at']=='2026-11-26T10:30'
    with pytest.raises(ValueError): add_appointment(db,1,pet,'','2026-11-26T10:30')
    with pytest.raises(ValueError): add_appointment(db,1,pet,'Vet','bad date')
    with pytest.raises(PermissionError): add_appointment(db,2,pet,'Vet','2026-11-26T10:30')

@pytest.mark.parametrize('delta,expected',[(-1,'Overdue'),(0,'Upcoming'),(1,'Upcoming'),(7,'Upcoming'),(8,None)])
def test_us09_date_rules(delta,expected):
    today=date(2026,11,25)
    assert reminder_status((today+timedelta(days=delta)).isoformat(),today)==expected

def test_us09_reminders(db):
    pet=save_pet(db,1,'Milo','Dog'); other=save_pet(db,2,'Kit','Cat')
    add_care(db,1,pet,'Medication','2026-11-20',due_date='2026-11-24')
    add_appointment(db,1,pet,'Today Vet','2026-11-25T10:30')
    add_appointment(db,1,pet,'Tomorrow Vet','2026-11-26T10:30')
    add_appointment(db,1,pet,'Later Vet','2026-12-04T10:30')
    add_appointment(db,2,other,'Other Vet','2026-11-26T10:30')
    assert [(r['title'],r['status']) for r in reminders(db,1,date(2026,11,25))]==[('Medication','Overdue'),('Today Vet','Upcoming'),('Tomorrow Vet','Upcoming')]
