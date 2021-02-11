from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError


class ViewCVForm(FlaskForm):
    graduate = IntegerField('graduate', validators=[DataRequired()])
    submit = SubmitField('View CV')
