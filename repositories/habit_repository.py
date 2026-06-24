from datetime import date
from database.connection import get_connection


def create_habit(name, description, start_date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO habits (name, description, start_date)
        VALUES (%s, %s, %s)
        RETURNING id;
        """,
        (name, description, start_date)
    )

    habit_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return habit_id


def list_habits():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, name, description, start_date, current_streak, best_streak, active
        FROM habits
        ORDER BY id;
        """
    )

    habits = cur.fetchall()

    cur.close()
    conn.close()

    return habits


def register_habit_log(habit_id, log_date, completed):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO habit_logs (habit_id, log_date, completed)
        VALUES (%s, %s, %s)
        ON CONFLICT (habit_id, log_date)
        DO UPDATE SET completed = EXCLUDED.completed;
        """,
        (habit_id, log_date, completed)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_habit_logs(habit_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT log_date, completed
        FROM habit_logs
        WHERE habit_id = %s
        ORDER BY log_date;
        """,
        (habit_id,)
    )

    logs = cur.fetchall()

    cur.close()
    conn.close()

    return logs


def update_streak(habit_id, current_streak, best_streak):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE habits
        SET current_streak = %s,
            best_streak = %s
        WHERE id = %s;
        """,
        (current_streak, best_streak, habit_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def delete_habit(habit_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM habits WHERE id = %s;", (habit_id,))

    conn.commit()
    cur.close()
    conn.close()