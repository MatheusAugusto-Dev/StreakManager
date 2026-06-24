from database.connection import get_connection


def create_goal(title, description, deadline=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO goals (title, description, deadline)
        VALUES (%s, %s, %s)
        RETURNING id;
        """,
        (title, description, deadline)
    )

    goal_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return goal_id


def list_goals():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, title, description, status, created_at, deadline
        FROM goals
        ORDER BY id;
        """
    )

    goals = cur.fetchall()

    cur.close()
    conn.close()

    return goals


def update_goal_status(goal_id, status):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE goals
        SET status = %s
        WHERE id = %s;
        """,
        (status, goal_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def delete_goal(goal_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM goals WHERE id = %s;", (goal_id,))

    conn.commit()
    cur.close()
    conn.close()