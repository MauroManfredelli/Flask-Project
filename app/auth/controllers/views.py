# app/auth/controllers/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from .. import auth
from ..forms.registration import RegistrationForm
from ..forms.login import LoginForm
from ... import db
from ...models.employee import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """ Handle request to the /register URL; add an employee to the database throught the registration form """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have succesfully registred! You may now login.')
        # redirect to the login page
        return redirect(url_for('auth.login'))
    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ Handle request to the /login URL; log an employee in through the login form """
    form = LoginForm()
    if form.validate_on_submit():
        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            # log employee in
            login_user(employee)
            # redirect to the dashboard page
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid email or password')
    return render_template('auth/login.html', form=form, title="Login")


@auth.route('/logout')
@login_required
def logout():
    """ Handle request to the /logout route; log an employee out throught the logout link """
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('auth.login'))