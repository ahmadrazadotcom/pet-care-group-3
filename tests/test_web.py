import re
import pytest
pytest.importorskip('flask')
from app import create_app

@pytest.fixture
def client(tmp_path):
    app=create_app({'TESTING':True,'DATABASE':str(tmp_path/'web.sqlite3'),'SECRET_KEY':'test-only'})
    return app.test_client()

def post(client,url,**fields):
    page=client.get(url)
    token=re.search(rb'name="csrf_token" value="([^"]+)"',page.data).group(1).decode()
    return client.post(url,data={**fields,'csrf_token':token},follow_redirects=True)

def account(client,email):
    assert b'Account created' in post(client,'/register',email=email,password='Password123').data
    assert b'My pets' in post(client,'/login',email=email,password='Password123').data

def test_us01_us02_access(client):
    assert client.get('/').status_code==302
    account(client,'one@example.com')
    assert b'This email is already registered' in post(client,'/register',email='one@example.com',password='Password123').data
    page=client.get('/')
    token=re.search(rb'name="csrf_token" value="([^"]+)"',page.data).group(1).decode()
    client.post('/logout',data={'csrf_token':token})
    assert client.get('/').status_code==302
    assert b'incorrect' in post(client,'/login',email='one@example.com',password='wrong').data

def test_us03_us04_us05_us07_us09_journey(client):
    account(client,'one@example.com')
    assert b'Milo' in post(client,'/pets/new',name='Milo',species='Dog').data
    assert b'Max' in post(client,'/pets/1/edit',name='Max',species='Dog').data
    assert b'Enter a pet name' in post(client,'/pets/1/edit',name='',species='Dog').data
    assert b'Vaccination' in post(client,'/pets/1/care/new',kind='Vaccination',care_date='2026-11-20',due_date='2026-11-25').data
    assert b'Sample Vet' in post(client,'/pets/1/appointments/new',clinic='Sample Vet',visit_at='2026-11-26T10:30').data
    with client.session_transaction() as s: s.clear()
    account(client,'two@example.com')
    assert b'Max' not in client.get('/').data
    for url in ['/pets/1','/pets/1/edit','/pets/1/care/new','/pets/1/appointments/new']:
        assert client.get(url).status_code==404

def test_csrf(client):
    assert client.post('/register',data={'email':'one@example.com','password':'Password123'}).status_code==400
