from datetime import date

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    height_cm = db.Column(db.Float)

    birth_date = db.Column(db.Date)

    workouts = db.relationship("Workout", backref="user", lazy=True)

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    date = db.Column(db.Date, nullable=False)

    duration_min = db.Column(db.Integer, nullable=False)

    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<Workout {self.id}>"

