import os
import secrets
import random
from PIL import Image
from flask import current_app, url_for
from donationsite import mail
from flask_mail import Message


def save_cv(form_cv):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_cv.filename)
    cv_fn = random_hex + f_ext
    cv_path = os.path.join(current_app.root_path, 'static/cvfiles', cv_fn)
    form_cv.save(cv_path)

    return cv_fn


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profilepics', picture_fn)
    output_size = (130, 130)
    i = Image.open(form_image)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset',
                  sender='graddonationsite@gmail.com', recipients=[user.email])
    msg.body = f'''To reset password, visit the following link:
{url_for('accounts.reset_password', token=token, _external=True)}

If you didn't make this requst, ignore this email.
'''
    mail.send(msg)
