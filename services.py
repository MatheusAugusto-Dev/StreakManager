import calendar
from datetime import date, timedelta
from models import Checkin


def has_valid_checkin(goal_id, target_date):
    return Checkin.query.filter_by(
        goal_id=goal_id,
        date=target_date
    ).first() is not None


def current_streak(goal):
    from datetime import date, timedelta

    today = date.today()
    streak = 0
    day = today

    while True:
        if not is_expected_day(goal, day):
            day -= timedelta(days=1)
            continue

        if has_valid_checkin(goal.id, day):
            streak += 1
            day -= timedelta(days=1)
        else:
            break

    return streak

def done_today(goal_id):
    return Checkin.query.filter_by(
        goal_id=goal_id,
        date=date.today()
    ).first() is not None

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

def is_expected_day(goal, target_date):
    if goal.frequency_type == "daily":
        return True

    if goal.frequency_type == "custom" and goal.start_date:
        delta_days = (target_date - goal.start_date).days
        cycle_day = delta_days % 3  

        return cycle_day in (0, 1)

    return True
