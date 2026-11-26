"""Small, proposed date rule for later dashboard work."""
from datetime import date, timedelta


def reminder_status(due: date, today: date, cancelled: bool = False) -> str:
    if cancelled:
        return "cancelled"
    if due < today:
        return "overdue"
    if due <= today + timedelta(days=7):
        return "upcoming"
    return "later"
