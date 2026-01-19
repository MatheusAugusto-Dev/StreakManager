from datetime import datetime, timedelta, date
from dateutil import parser

def get_current_week_range():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # segunda
    end_of_week = start_of_week + timedelta(days=6)          # domingo
    return start_of_week, end_of_week


def is_date_in_current_week(iso_datetime: str) -> bool:
    """
    Recebe uma data ISO da API (ex: 2026-01-19T16:21:07+00:00)
    """
    workout_date = parser.isoparse(iso_datetime).date()
    start, end = get_current_week_range()
    return start <= workout_date <= end
