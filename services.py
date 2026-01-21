import calendar
from datetime import date, timedelta
from integrations.hevy.utils import is_valid_checkin
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

def weekly_streak(goal):
    from datetime import date, timedelta
    from models import Checkin

    today = date.today()
    streak = 0
    week_cursor = week_key(today)

    while True:
        # todos os checkins válidos da semana
        checkins = (
            Checkin.query
            .filter(Checkin.goal_id == goal.id)
            .filter(Checkin.is_rest_day == False)
            .all()
        )

        week_map = {}
        for c in checkins:
            wk = week_key(c.date)
            week_map.setdefault(wk, 0)
            week_map[wk] += 1

        # se a semana atual não tem registros suficientes → quebra
        if week_map.get(week_cursor, 0) < (goal.weekly_target or 1):
            break

        streak += 1

        # volta uma semana
        year, week = map(int, week_cursor.replace("W", "-").split("-")[0:2])
        prev_date = date.fromisocalendar(year, week, 1) - timedelta(days=7)
        week_cursor = week_key(prev_date)

    return streak


def current_streak(goal):
    if goal.frequency_type == "weekly":
        return weekly_streak(goal)

    from datetime import date, timedelta
    from models import Checkin

    today = date.today()
    streak = 0
    d = today

    while True:
        checkin = Checkin.query.filter_by(goal_id=goal.id, date=d).first()

        # descanso manual
        if checkin and checkin.is_rest_day:
            d -= timedelta(days=1)
            continue

        # dias fixos da semana
        if goal.frequency_type == "weekly_days":
            if not goal.allowed_weekdays or d.weekday() not in goal.allowed_weekdays:
                d -= timedelta(days=1)
                continue

        # domingo opcional
        if d.weekday() == 6 and goal.sunday_optional:
            d -= timedelta(days=1)
            continue

        # precisa ter check-in válido
        if checkin:
            streak += 1
            d -= timedelta(days=1)
        else:
            break

    return streak


def current_weekly_streak(goal) -> int:
    from datetime import date, timedelta

    today = date.today()
    streak = 0

    # começamos pela semana atual
    week_start = today - timedelta(days=today.weekday())

    while True:
        week_end = week_start + timedelta(days=6)

        # houve execução válida nesta semana?
        checkins = Checkin.query.filter(
            Checkin.goal_id == goal.id,
            Checkin.date >= week_start,
            Checkin.date <= week_end,
            Checkin.is_rest_day == False
        ).all()

        if checkins:
            streak += 1
            week_start -= timedelta(days=7)
        else:
            break

    return streak

def weekly_days_streak(goal) -> int:
    from datetime import date, timedelta
    from models import Checkin

    streak = 0
    d = date.today()

    while True:
        checkin = Checkin.query.filter_by(
            goal_id=goal.id,
            date=d
        ).first()

        # descanso manual → neutro
        if checkin and checkin.is_rest_day:
            d -= timedelta(days=1)
            continue

        # dia não esperado → neutro
        if not is_expected_day(goal, d):
            d -= timedelta(days=1)
            continue

        # dia esperado → precisa de execução válida
        if checkin and is_valid_checkin(goal, checkin):
            streak += 1
            d -= timedelta(days=1)
            continue

        break

    return streak


def daily_streak(goal) -> int:
    from datetime import date, timedelta
    from models import Checkin

    streak = 0
    d = date.today()

    while True:
        checkin = Checkin.query.filter_by(
            goal_id=goal.id,
            date=d
        ).first()

        if checkin and checkin.is_rest_day:
            d -= timedelta(days=1)
            continue

        if checkin and is_valid_checkin(goal, checkin):
            streak += 1
            d -= timedelta(days=1)
        else:
            break

    return streak

def week_key(d: date):
    year, week, _ = d.isocalendar()
    return f"{year}-W{week}"