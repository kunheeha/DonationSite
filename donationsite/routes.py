from flask import render_template, request, url_for, flash, redirect
from donationsite import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required
from donationsite.forms import RegistrationForm, LoginForm
from donationsite.models import User, Role, UserRoles, Degree, UserDegree, Bankdetails, UserBankdetails


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/makedonation')
def makedonation():
    return render_template("makedonation.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('account'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # gradrole = Role.query.filter_by(name='Graduate').first()
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data,
                    password=hashed_password)
        # user.roles.append(gradrole)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}', 'success')
        return redirect(url_for('account'))
    return render_template("register.html", title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/account')
def account():
    return render_template("account.html")
