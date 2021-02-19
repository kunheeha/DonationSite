from donationsite import mail
from flask_mail import Message


def donateinfo_email(donateTo):
    msg = Message('Donation Received',
                  sender='graddonationsite@gmail.com', recipients=['graddonationsite@gmail.com'])
    msg.body = "Donation received for " + donateTo
    mail.send(msg)
