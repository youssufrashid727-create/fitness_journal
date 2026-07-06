from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.auth.forms import RegisterForm, LoginForm
from werkzeug.security import check_password_hash
from flask import session

from app.auth.forms import RegisterForm
from app.models import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(username=form.username.data).first()

        if existing_user:
            flash("Username already exists.", "danger")
            return redirect(url_for("auth.register"))

        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_email:
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password,
            height_cm=form.height_cm.data,
            birth_date=form.birth_date.data
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/register.html",
        form=form
    )
    


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        print("FORM SUBMITTED")

        user = User.query.filter_by(email=form.email.data).first()

        print(user)

        if user and check_password_hash(user.password_hash, form.password.data):

            print("PASSWORD CORRECT")

            session["user_id"] = user.id
            session["username"] = user.username

            flash("Welcome back!", "success")

            return redirect(url_for("main.home"))

        flash("Invalid email or password.", "danger")

    else:
        print(form.errors)

    return render_template(
        "auth/login.html",
        form=form
    )

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "info")

    return redirect(url_for("main.home"))