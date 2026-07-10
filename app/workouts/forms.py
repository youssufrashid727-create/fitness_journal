from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class WorkoutForm(FlaskForm):

    date = DateField(
        "Workout Date",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    duration_min = IntegerField(
        "Duration (minutes)",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    notes = TextAreaField("Notes")

    submit = SubmitField("Save Workout")