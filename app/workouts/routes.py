from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.workouts.forms import WorkoutForm
from app.models import Workout
from app.extensions import db
from app.auth.decorators import login_required


workout_bp = Blueprint("workout", __name__)


@workout_bp.route("/workouts", methods=["GET", "POST"])
@login_required
def workouts():

    form = WorkoutForm()

    if form.validate_on_submit():

        workout = Workout(
            user_id=session["user_id"],
            date=form.date.data,
            duration_min=form.duration_min.data,
            notes=form.notes.data
        )

        db.session.add(workout)
        db.session.commit()

        flash("Workout added successfully!", "success")

        return redirect(url_for("workout.workouts"))

    workouts = Workout.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "workouts/workouts.html",
        form=form,
        workouts=workouts
    )


@workout_bp.route("/workouts/edit/<int:workout_id>", methods=["GET", "POST"])
@login_required
def edit_workout(workout_id):

    workout = Workout.query.get_or_404(workout_id)

    if workout.user_id != session["user_id"]:
        flash("Access denied.", "danger")
        return redirect(url_for("workout.workouts"))

    form = WorkoutForm(obj=workout)

    if form.validate_on_submit():

        workout.date = form.date.data
        workout.duration_min = form.duration_min.data
        workout.notes = form.notes.data

        db.session.commit()

        flash("Workout updated!", "success")

        return redirect(url_for("workout.workouts"))

    return render_template(
        "workouts/edit_workout.html",
        form=form
    )


@workout_bp.route("/workouts/delete/<int:workout_id>")
@login_required
def delete_workout(workout_id):

    workout = Workout.query.get_or_404(workout_id)

    if workout.user_id != session["user_id"]:
        flash("Access denied.", "danger")
        return redirect(url_for("workout.workouts"))

    db.session.delete(workout)
    db.session.commit()

    flash("Workout deleted!", "success")

    return redirect(url_for("workout.workouts"))