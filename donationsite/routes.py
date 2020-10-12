import os
import secrets
import random
from PIL import Image
from flask import render_template, request, url_for, flash, redirect, jsonify, send_from_directory
from donationsite import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required
from donationsite.forms import RegistrationForm, LoginForm, AddCVForm, AddImageForm, AddDegreeForm, AddAboutForm, BankDetailForm, ViewCVForm
from donationsite.models import User, Role, UserRoles, Degree, UserDegree, Bankdetails, UserBankdetails


@app.route('/', methods=['GET', 'POST'])
def index():
    grads = User.query.all()

    if request.method == 'POST':
        received = request.form['gradId']
        global gradid
        gradid = int(received)

    return render_template("index.html", grads=grads)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    grad = User.query.filter_by(id=gradid).first()
    image_file = url_for(
        'static', filename='profilepics/' + grad.image_file)

    return render_template('profile.html', grad=grad, image_file=image_file)


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
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Account created for {form.name.data}, please log in', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_cv(form_cv):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_cv.filename)
    cv_fn = random_hex + f_ext
    cv_path = os.path.join(app.root_path, 'static/cvfiles', cv_fn)
    form_cv.save(cv_path)

    return cv_fn


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profilepics', picture_fn)
    output_size = (130, 130)
    i = Image.open(form_image)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    cvform = AddCVForm()
    imageform = AddImageForm()
    aboutform = AddAboutForm()
    degreeform = AddDegreeForm()
    viewcvform = ViewCVForm()

    if cvform.validate_on_submit():
        if not current_user.cv_file:
            if cvform.cv_file.data:
                cv = save_cv(cvform.cv_file.data)
                current_user.cv_file = cv
                db.session.commit()
                flash('Your CV has been uploaded', 'success')
        elif current_user.cv_file:
            if cvform.cv_file.data:
                cvfilename = current_user.cv_file
                path = os.path.join(
                    app.root_path, 'static/cvfiles', cvfilename)
                os.remove(path)
                cv = save_cv(cvform.cv_file.data)
                current_user.cv_file = cv
                db.session.commit()
                flash('Your CV has been uploaded', 'success')

    if imageform.validate_on_submit():
        if imageform.image_file.data:
            pp = save_image(imageform.image_file.data)
            current_user.image_file = pp
            db.session.commit()
            flash('Your profile photo has been updated', 'success')

    if aboutform.validate_on_submit():
        current_user.self_desc = aboutform.self_desc.data
        db.session.commit()
        flash('Profile updated', 'success')
    elif request.method == 'GET':
        if current_user.self_desc:
            aboutform.self_desc.data = current_user.self_desc

    if degreeform.validate_on_submit():
        degree = Degree(title=degreeform.title.data,
                        institution=degreeform.institution.data, grad_year=degreeform.grad_year.data)
        db.session.add(degree)
        db.session.commit()
        userdegree = Degree.query.filter_by(
            title=degreeform.title.data, institution=degreeform.institution.data, grad_year=degreeform.grad_year.data).first()
        current_user.degree = []
        current_user.degree.append(userdegree)
        db.session.commit()
        flash('Your degree has been updated', 'success')
    elif request.method == 'GET':
        if current_user.degree != []:
            usrdegree = current_user.degree[0]
            degreeform.title.data = usrdegree.title
            degreeform.institution.data = usrdegree.institution
            degreeform.grad_year.data = usrdegree.grad_year

    if viewcvform.validate_on_submit():
        cvgradid = viewcvform.graduate.data
        cvgrad = User.query.filter_by(id=cvgradid).first()
        cvfile = cvgrad.cv_file
        cvfiles = os.path.join(app.root_path, 'static/cvfiles')
        return send_from_directory(directory=cvfiles, filename=cvfile)

    image_file = url_for(
        'static', filename='profilepics/' + current_user.image_file)

    return render_template("account.html", aboutform=aboutform, cvform=cvform, imageform=imageform, degreeform=degreeform, image_file=image_file, viewcvform=viewcvform)


@app.route('/bankdetails', methods=['GET', 'POST'])
def bankdetails():
    form = BankDetailForm()

    if form.validate_on_submit():
        accountNumber = str(form.account_number.data)
        sortCode = str(form.sortcode.data)
        bank = Bankdetails(account_holder=form.account_holder.data,
                           account_number=accountNumber, sort_code=sortCode)
        db.session.add(bank)
        db.session.commit()
        usrbank = Bankdetails.query.filter_by(
            account_number=accountNumber).first()
        current_user.bank_details = []
        current_user.bank_details.append(usrbank)
        db.session.commit()
        flash('Your bank details have been updated', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        if current_user.bank_details != []:
            userbank = current_user.bank_details[0]
            form.account_holder.data = userbank.account_holder
            form.account_number.data = userbank.account_number
            form.sortcode.data = userbank.sort_code

    return render_template('bankdetails.html', form=form)


@app.route('/testing', methods=['GET', 'POST'])
def testing():
    form = AddAboutForm()

    if form.validate_on_submit():
        desc = form.self_desc.data
        current_user.self_desc = desc
        db.session.add(current_user)
        db.session.commit()

    return render_template('testing.html', form=form)
