from flask import render_template, request, url_for, flash, redirect
from donationsite import app
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required


@app.route('/')
def index():
    return render_template("index.html")
