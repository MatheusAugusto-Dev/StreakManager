from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Integer

db = SQLAlchemy()


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))

    color = db.Column(db.String(20), default="#4CAF50")

    # Métrica (tempo/páginas/capítulos)
    metric_type = db.Column(db.String(20), default="time", nullable=False)
    target_value = db.Column(db.Integer, default=0, nullable=False)

    # Frequência:
    # daily        -> todos os dias
    # weekly       -> X vezes por semana (flexível)
    # weekly_days  -> dias fixos da semana (ex: seg, ter, qui, sex, sáb)
    # custom       -> regras específicas (ex: seu ciclo antigo)
    frequency_type = db.Column(db.String(20), default="daily", nullable=False)

    # weekly (flexível): quantas vezes por semana
    weekly_target = db.Column(db.Integer, nullable=True)

    # weekly_days (dias fixos): lista de weekday ints (segunda=0 ... domingo=6)
    allowed_weekdays = db.Column(ARRAY(Integer), nullable=True)

    # custom (se ainda usar): data base do ciclo
    start_date = db.Column(db.Date, nullable=True)

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.Date, default=date.today)
    sunday_optional = db.Column(db.Boolean, default=False)


    checkins = db.relationship(
        "Checkin",
        backref="goal",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Goal {self.title}>"


class Checkin(db.Model):
    __tablename__ = "checkins"

    id = db.Column(db.Integer, primary_key=True)

    goal_id = db.Column(
        db.Integer,
        db.ForeignKey("goals.id", ondelete="CASCADE"),
        nullable=False
    )

    date = db.Column(db.Date, nullable=False)

    # progresso do dia: minutos/páginas/capítulos
    progress_value = db.Column(db.Integer, default=0, nullable=False)

    focus_level = db.Column(db.Integer)
    notes = db.Column(db.Text)

    is_rest_day = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.UniqueConstraint("goal_id", "date", name="uix_goal_date"),
    )

    def __repr__(self):
        return f"<Checkin goal={self.goal_id} date={self.date}>"
