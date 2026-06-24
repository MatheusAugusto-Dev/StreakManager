from datetime import date, timedelta
from repositories.habit_repository import (
    register_habit_log,
    get_habit_logs,
    update_streak
)


def mark_habit(habit_id, completed, log_date=None):
    if log_date is None:
        log_date = date.today()

    register_habit_log(habit_id, log_date, completed)
    recalculate_streak(habit_id)


def recalculate_streak(habit_id):
    logs = get_habit_logs(habit_id)

    completed_dates = {
        log_date for log_date, completed in logs if completed
    }

    if not completed_dates:
        update_streak(habit_id, 0, 0)
        return

    last_completed_day = max(completed_dates)

    current_streak = 0
    cursor_day = last_completed_day

    while cursor_day in completed_dates:
        current_streak += 1
        cursor_day -= timedelta(days=1)

    best_streak = calculate_best_streak(completed_dates)

    update_streak(habit_id, current_streak, best_streak)

def calculate_best_streak(completed_dates):
    if not completed_dates:
        return 0

    sorted_dates = sorted(completed_dates)

    best = 1
    current = 1

    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] == sorted_dates[i - 1] + timedelta(days=1):
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best