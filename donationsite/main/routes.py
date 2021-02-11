from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify, send_from_directory, current_app
import os
from donationsite.models import User
from donationsite.main.forms import ViewCVForm

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    grads = User.query.all()

    if request.method == 'POST':
        received = request.form['gradId']
        global gradid
        gradid = int(received)

    return render_template("index.html", grads=grads)


@main.route('/profile', methods=['GET', 'POST'])
def profile():
    grad = User.query.filter_by(id=gradid).first()
    image_file = url_for(
        'static', filename='profilepics/' + grad.image_file)

    viewcvform = ViewCVForm()
    if viewcvform.validate_on_submit():
        cvgradid = viewcvform.graduate.data
        cvgrad = User.query.filter_by(id=cvgradid).first()
        cvfile = cvgrad.cv_file
        cvfiles = os.path.join(current_app.root_path, 'static/cvfiles')
        return send_from_directory(directory=cvfiles, filename=cvfile)

    return render_template('profile.html', grad=grad, image_file=image_file, viewcvform=viewcvform)
