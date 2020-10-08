from flask import render_template, request, url_for, flash, redirect
from donationsite import app
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required
from donationsite.forms import RegistrationForm, LoginForm


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/makedonation')
def makedonation():
    return render_template("makedonation.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'kunheeha@gmail.com' and form.password.data == 'gkrjsgml':
            flash('You have been logged in', 'success')
            return redirect(url_for('account'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.name.data}', 'success')
        return redirect(url_for('account'))
    return render_template("register.html", title='Register', form=form)


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/account')
def account():
    return render_template("account.html")
