from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))

    color = db.Column(db.String(20), default="#4CAF50")

    metric_type = db.Column(
        db.String(20),
        default="time",
        nullable=False
    )

    target_value = db.Column(db.Integer, default=0)

    frequency_type = db.Column(
        db.String(20),
        default="daily",
        nullable=False
    )

    start_date = db.Column(db.Date)

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.Date, default=date.today)

    checkins = db.relationship(
        "Checkin",
        backref="goal",
        cascade="all, delete-orphan"
    )


class Checkin(db.Model):
    __tablename__ = "checkins"

    id = db.Column(db.Integer, primary_key=True)

    goal_id = db.Column(
        db.Integer,
        db.ForeignKey("goals.id", ondelete="CASCADE"),
        nullable=False
    )

    date = db.Column(db.Date, nullable=False)

    progress_value = db.Column(db.Integer, default=0)

    focus_level = db.Column(db.Integer)
    notes = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint("goal_id", "date", name="uix_goal_date"),
    )
