import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, UserMixin
from flask_admin import Admin, AdminIndexView
from donationsite.config import Config
import stripe


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('Admin'):
            return True
        else:
            return False


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin(index_view=MyAdminIndexView())

stripe_keys = {
    "publishable_key": os.environ.get("STRIPE_PUBLISHABLE_KEY"),
    "secret_key": os.environ.get("STRIPE_SECRET_KEY")
}

stripe.api_key = stripe_keys["secret_key"]


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    from donationsite.accounts.routes import accounts
    from donationsite.donations.routes import donations
    from donationsite.main.routes import main

    app.register_blueprint(accounts)
    app.register_blueprint(donations)
    app.register_blueprint(main)

    return app
