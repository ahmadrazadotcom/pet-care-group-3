import threading
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pytest
pytest.importorskip('flask')
from werkzeug.serving import make_server
from playwright.sync_api import sync_playwright
from app import create_app

@pytest.mark.e2e
def test_browser_owner_journey(tmp_path):
    app=create_app({'DATABASE':str(tmp_path/'browser.sqlite3'),'SECRET_KEY':'test-only'})
    server=make_server('127.0.0.1',0,app)
    thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    today=datetime.now(ZoneInfo('Australia/Sydney')).date()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            page=browser.new_page()
            page.goto(base+'/register'); page.get_by_label('Email address').fill('demo@example.com'); page.get_by_label('Password').fill('Password123'); page.get_by_role('button',name='Create account').click()
            page.get_by_label('Email address').fill('demo@example.com'); page.get_by_label('Password').fill('Password123'); page.get_by_role('button',name='Sign in').click()
            page.get_by_role('link',name='Add a pet').click(); page.get_by_label('Pet name').fill('Milo'); page.get_by_label('Species').fill('Dog'); page.get_by_role('button',name='Save pet').click()
            page.get_by_role('link',name='Edit pet').click(); page.get_by_label('Pet name').fill('Max'); page.get_by_role('button',name='Save pet').click()
            page.get_by_role('link',name='Add care record').click(); page.get_by_label('Care type').select_option('Vaccination'); page.get_by_label('Care date').fill((today-timedelta(days=2)).isoformat()); page.get_by_label('Next due date (optional)').fill((today-timedelta(days=1)).isoformat()); page.get_by_role('button',name='Save care record').click()
            page.get_by_role('link',name='Add appointment').click(); page.get_by_label('Clinic name').fill('Sample Vet'); page.get_by_label('Appointment date and time (Sydney time)').fill(today.isoformat()+'T10:30'); page.get_by_role('button',name='Save appointment').click()
            page.get_by_role('link',name='Dashboard').click(); assert page.get_by_text('Overdue',exact=True).count()==1; assert page.get_by_text('Upcoming',exact=True).count()==1
            page.get_by_role('button',name='Sign out').click(); page.goto(base+'/pets/1'); assert '/login' in page.url
            browser.close()
    finally:
        server.shutdown(); thread.join(timeout=5)
