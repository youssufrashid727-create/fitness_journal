from flask import Blueprint, render_template, session
from app.auth.decorators import login_required
from app.models import Workout

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():

    workouts = Workout.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Workout.date.desc()).all()

    return render_template(
        "dashboard.html",
        workouts=workouts
    )