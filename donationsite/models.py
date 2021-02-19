from donationsite import db, admin, login_manager
from flask import current_app
from flask_login import UserMixin, current_user
from flask_admin import AdminIndexView
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    cv_file = db.Column(db.String(20), nullable=True)
    goals = db.Column(db.String(240), nullable=True)
    self_desc = db.Column(db.String(240), nullable=True)
    degree = db.relationship('Degree', secondary='user_degree')
    bank_details = db.relationship('Bankdetails', secondary='user_bankdetails')
    roles = db.relationship('Role', secondary='user_roles')

    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"Role('{self.name}')"


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"UserRoles('{self.user_id}', '{self.role_id}')"


class Degree(db.Model):
    __tablename__ = 'degree'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    institution = db.Column(db.String(120), nullable=False)
    grad_year = db.Column(db.String(4), nullable=False)

    def __repr__(self):
        return f"Degree('{self.title}')"


class UserDegree(db.Model):
    __tablename__ = 'user_degree'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    degree_id = db.Column(db.Integer(), db.ForeignKey(
        'degree.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"UserDegree('{self.user_id}')"


class Bankdetails(db.Model):
    __tablename__ = 'bankdetails'
    id = db.Column(db.Integer(), primary_key=True)
    account_holder = db.Column(db.String(30), nullable=False, unique=False)
    account_number = db.Column(db.String(10), nullable=False, unique=False)
    sort_code = db.Column(db.String(10), nullable=False, unique=False)

    def __repr__(self):
        return f"Bankdetails('{self.account_holder}')"


class UserBankdetails(db.Model):
    __tablename__ = 'user_bankdetails'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    bankdetails_id = db.Column(db.Integer(), db.ForeignKey(
        'bankdetails.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"UserBankdetails('{self.user_id}')"


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('Admin'):
            return True
        else:
            return False


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('Admin'):
            return True
        else:
            return False


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(Degree, db.session))
admin.add_view(MyModelView(Bankdetails, db.session))
