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

def is_valid_checkin(goal, checkin) -> bool:
    """
    Retorna True se o check-in deve contar como execução válida da meta.
    A regra é simples: se NÃO é descanso e tem progresso positivo.
    """

    if checkin.is_rest_day:
        return False

    # progresso precisa existir e ser maior que zero
    if checkin.progress_value is None:
        return False

    return checkin.progress_value > 0
