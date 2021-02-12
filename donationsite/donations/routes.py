from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from donationsite import stripe_keys
from donationsite.models import User, Bankdetails, UserBankdetails
import stripe


donations = Blueprint('donations', __name__)


@donations.route('/makedonation')
def makedonation():
    grads = User.query.all()

    return render_template("makedonation.html", grads=grads)


# @donations.route('/getkey')
# def get_publishable_key():
#     stripe_config = {"publicKey": stripe_keys["publishable_key"]}
#     return jsonify(stripe_config)

stripe.api_key = stripe_keys['secret_key']


@donations.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                                'name': '£5 Donation',
                    },
                    'unit_amount': 500,
                    },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:5000/success',
        cancel_url='http://localhost:5000/cancel',
    )

    return jsonify(id=session.id)


@donations.route('/success')
def thanks():
    return render_template("thanks.html")


@donations.route('/cancel')
def cancel():
    return render_template("donate.html")


@donations.route('/donate')
def donate():
    return render_template("donate.html")
