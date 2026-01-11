import calendar
from datetime import date, timedelta
from models import Checkin

def monthly_calendar(goal_id, year=None, month=None):
    today = date.today()

    year = year or today.year
    month = month or today.month

    cal = calendar.Calendar()
    days = cal.itermonthdates(year, month)

    checkins = {
        c.date for c in Checkin.query.filter_by(goal_id=goal_id).all()
    }

    calendar_days = []

    for day in days:
        if day.month != month:
            continue

        calendar_days.append({
            "day": day.day,
            "date": day,
            "done": day in checkins,
            "is_today": day == today
        })

    return calendar_days

def week_key(d: date):
    return d.isocalendar().year, d.isocalendar().week

def weekly_progress(goal, target_date):
    year, week = week_key(target_date)

    return Checkin.query.filter(
        Checkin.goal_id == goal.id,
        Checkin.date >= date.fromisocalendar(year, week, 1),
        Checkin.date <= date.fromisocalendar(year, week, 7)
    ).count()

def has_valid_checkin(goal_id: int, target_date: date) -> bool:
    return (
        Checkin.query.filter_by(goal_id=goal_id, date=target_date).first()
        is not None
    )

def week_start_end(d: date):
    start = d - timedelta(days=d.weekday())  # segunda
    end = start + timedelta(days=6)          # domingo
    return start, end

def done_today(goal_id: int) -> bool:
    today = date.today()
    return Checkin.query.filter_by(goal_id=goal_id, date=today).first() is not None

def has_checkin(goal_id: int, d: date) -> bool:
    return Checkin.query.filter_by(goal_id=goal_id, date=d).first() is not None

def is_expected_day(goal, d: date) -> bool:
    # Domingo opcional (dia neutro)
    if goal.sunday_optional and d.weekday() == 6:
        return False

    # Dias fixos
    if goal.frequency_type == "weekly_days":
        if not goal.allowed_weekdays:
            return False
        return d.weekday() in goal.allowed_weekdays

    # Ciclo antigo (se ainda existir)
    if goal.frequency_type == "custom" and goal.start_date:
        delta = (d - goal.start_date).days
        return (delta % 3) in (0, 1)

    # daily / weekly flexível
    return True

def weekly_streak(goal) -> int:
    """
    Streak por semanas consecutivas bem-sucedidas.
    Semana bem-sucedida = quantidade de check-ins na semana >= weekly_target
    """
    if not goal.weekly_target:
        return 0

    streak = 0
    cursor = date.today()

    while True:
        start, end = week_start_end(cursor)
        count = Checkin.query.filter(
            Checkin.goal_id == goal.id,
            Checkin.date >= start,
            Checkin.date <= end
        ).count()

        if count >= goal.weekly_target:
            streak += 1
            cursor -= timedelta(days=7)
        else:
            break

    return streak

def current_streak(goal) -> int:
    from datetime import date, timedelta

    if goal.frequency_type == "weekly":
        return weekly_streak(goal)

    today = date.today()
    streak = 0
    d = today

    while True:
        checkin = Checkin.query.filter_by(goal_id=goal.id, date=d).first()

        # Descanso manual → neutro
        if checkin and checkin.is_rest_day:
            d -= timedelta(days=1)
            continue

        # Dias neutros automáticos
        if goal.frequency_type in ("weekly_days", "custom"):
            if not is_expected_day(goal, d):
                d -= timedelta(days=1)
                continue

        # Dia esperado → precisa de check-in
        if checkin:
            streak += 1
            d -= timedelta(days=1)
        else:
            break

    return streak
