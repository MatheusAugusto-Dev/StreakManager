from datetime import date, timedelta
from models import Goal, Checkin


def get_current_week_range():
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start, end


def get_weekly_stats():
    start, end = get_current_week_range()

    goals = Goal.query.filter_by(is_active=True).all()
    result = []

    for goal in goals:
        checkins = Checkin.query.filter(
            Checkin.goal_id == goal.id,
            Checkin.date >= start,
            Checkin.date <= end
        ).all()

        total = sum(c.progress_value for c in checkins)
        count = len(checkins)

        # esperado
        if goal.frequency_type == "daily":
            expected = 7
        elif goal.frequency_type == "weekly":
            expected = goal.weekly_target or 0
        else:
            expected = None  # custom (academia)

        result.append({
            "title": goal.title,
            "metric_type": goal.metric_type,
            "target_value": goal.target_value,
            "total": total,
            "count": count,
            "expected": expected
        })

    return {
        "start": start,
        "end": end,
        "goals": result
    }
