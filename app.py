from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Goal, Checkin
from datetime import date, datetime
from services import current_streak, done_today, current_streak, is_expected_day, monthly_calendar
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def dashboard():
    goals = Goal.query.filter_by(is_active=True).all()

    goals_data = []

    for goal in goals:
        goals_data.append({
            "id": goal.id,
            "title": goal.title,
            "category": goal.category,
            "color": goal.color,

            "metric_type": goal.metric_type,
            "target_value": goal.target_value,

            "frequency_type": goal.frequency_type,
            "weekly_target": goal.weekly_target, 

            "streak": current_streak(goal),
            "done_today": done_today(goal.id),
        })

    return render_template("dashboard.html", goals=goals_data)

@app.route("/goals/new", methods=["GET", "POST"])
def new_goal():
    if request.method == "POST":
        frequency_type = request.form["frequency_type"]

        start_date = None
        weekly_target = None
        if frequency_type == "weekly":
            weekly_target = int(request.form["weekly_target"])

        if frequency_type == "custom":
            start_date_str = request.form.get("start_date")
            if start_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

        goal = Goal(
            title=request.form["title"],
            category=request.form["category"],
            color=request.form.get("color", "#4CAF50"),
            metric_type=request.form["metric_type"],
            target_value=int(request.form["target_value"]),
            frequency_type=frequency_type,
            start_date=start_date,
            weekly_target=weekly_target
        )

        db.session.add(goal)
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("goal_form.html")


@app.route("/goals/<int:goal_id>/checkin", methods=["GET", "POST"])
def checkin(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    today = date.today()

    if goal.frequency_type == "custom":
        if not is_expected_day(goal, today):
            return (
                "❌ Hoje é um dia de descanso dessa meta. "
                "Ela não conta nem quebra o streak.",
                400
            )

    checkin = Checkin.query.filter_by(
        goal_id=goal.id,
        date=today
    ).first()

    if request.method == "POST":
        try:
            progress_value = int(request.form.get("progress_value", 0))
        except ValueError:
            return "❌ Valor inválido", 400

        focus = request.form.get("focus_level")
        notes = request.form.get("notes")

        if progress_value < goal.target_value:
            return (
                f"❌ Progresso mínimo não atingido. "
                f"Esperado: {goal.target_value}",
                400
            )

        if not checkin:
            checkin = Checkin(
                goal_id=goal.id,
                date=today
            )
            db.session.add(checkin)

        checkin.progress_value = progress_value
        checkin.focus_level = int(focus) if focus else None
        checkin.notes = notes

        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("checkin_form.html",goal=goal,checkin=checkin)

@app.route("/goals/<int:goal_id>")
def goal_detail(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    calendar_days = monthly_calendar(goal.id)

    return render_template(
        "goal_detail.html",
        goal=goal,
        calendar_days=calendar_days
    )

@app.route("/goals/<int:goal_id>/delete", methods=["POST"])
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    goal.is_active = False
    db.session.commit()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
