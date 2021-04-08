from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from donationsite import stripe_keys
from donationsite.models import User, Bankdetails, UserBankdetails
import stripe
from donationsite.donations.utils import donateinfo_email


donations = Blueprint('donations', __name__)


@donations.route('/makedonation')
def makedonation():

    q = request.args.get('q', type=str)
    if q:
        print(q)
        grads = User.query.filter(User.name.contains(q)).all()
    else:
        grads = User.query.all()

    return render_template("makedonation.html", grads=grads)


stripe.api_key = stripe_keys['secret_key']


@donations.route('/create-checkout-session/<donatedTo>', methods=['POST'])
def create_checkout_session(donatedTo):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                                'name': '£5 Donation',
                                'description': donatedTo
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


@donations.route('/success', methods=['POST', 'GET'])
def thanks():
    return render_template("thanks.html")


@donations.route('/cancel')
def cancel():
    return render_template("cancel.html")
