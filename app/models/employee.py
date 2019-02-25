# app/models/employee.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

# we make use of some of Werkzeug's handy security helper methods, generate_password_hash, which allows us to hash
# passwords, and check_password_hash, which allows us ensure the hashed password matches the password. To enhance
# security, we have a password method which ensures that the password can never be accessed; instead an error will be
# raised. We also have two foreign key fields, department_id and role_id, which refer to the ID's of the department and
# role assigned to the employee.

class Employee(UserMixin, db.Model):
    """Create an Employee table"""

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self, password):
        """ Prevnt password from being accessed """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """ Set password to a hashed password """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ Check if hashed password matches actual password """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))