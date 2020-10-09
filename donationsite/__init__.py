from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, UserMixin
from flask_admin import Admin, AdminIndexView


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('Admin'):
            return True
        else:
            return False


app = Flask(__name__)
app.config['SECRET_KEY'] = '91da41a4b94ec02afceef24cd35a8d54'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
admin = Admin(app, index_view=MyAdminIndexView())


from donationsite import routes
