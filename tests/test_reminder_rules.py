from datetime import date
from reminder_rules import reminder_status

TODAY = date(2026, 11, 26)

def test_past_date():
    assert reminder_status(date(2026, 11, 25), TODAY) == "overdue"

def test_today():
    assert reminder_status(TODAY, TODAY) == "upcoming"

def test_tomorrow():
    assert reminder_status(date(2026, 11, 27), TODAY) == "upcoming"

def test_later():
    assert reminder_status(date(2026, 12, 4), TODAY) == "later"

def test_cancelled():
    assert reminder_status(date(2026, 11, 25), TODAY, True) == "cancelled"
