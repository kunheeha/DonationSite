from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from donationsite import stripe_keys
from donationsite.models import User, Bankdetails, UserBankdetails

donations = Blueprint('donations', __name__)


@donations.route('/makedonation')
def makedonation():
    grads = User.query.all()

    return render_template("makedonation.html", grads=grads)


@donations.route('/getkey')
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@donations.route('/thanks')
def thanks():
    return render_template("thanks.html")


@donations.route('/donate')
def donate():
    return render_template("donate.html")
