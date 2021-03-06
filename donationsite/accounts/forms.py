from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from donationsite.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class AddCVForm(FlaskForm):
    cv_file = FileField('Add CV', validators=[
                        FileAllowed(['doc', 'docx', 'pdf'])])
    submit = SubmitField('Upload')


class AddImageForm(FlaskForm):
    image_file = FileField('Update Profile Picture', validators=[
                           FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Upload')


class AddAboutForm(FlaskForm):
    self_desc = StringField('About', validators=[
                            DataRequired()])
    submit = SubmitField('Save')


class AddDegreeForm(FlaskForm):
    title = StringField('Degree Title', validators=[
                        DataRequired(), Length(min=5, max=120)])
    institution = StringField('Institution', validators=[
                              DataRequired(), Length(min=5, max=120)])
    grad_year = StringField('Graduation Year', validators=[
                            DataRequired(), Length(min=4, max=4)])
    submit = SubmitField('Save')


class BankDetailForm(FlaskForm):
    account_holder = StringField('Account Holder', validators=[
                                 DataRequired(), Length(min=2, max=30)])
    account_number = IntegerField('Account Number', validators=[
        DataRequired()])
    sortcode = IntegerField('Sort Code', validators=[
        DataRequired()])
    submit = SubmitField('Save')


class ViewCVForm(FlaskForm):
    graduate = IntegerField('graduate', validators=[DataRequired()])
    submit = SubmitField('View CV')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account with that email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
