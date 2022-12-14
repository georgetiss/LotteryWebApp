# IMPORTS
import logging

from flask import Blueprint, render_template, flash, redirect, url_for, request
from datetime import datetime
from app import db
from models import User
from users.forms import RegisterForm
from users.forms import LoginForm
import bcrypt
from cryptography.fernet import Fernet
from flask import session
from flask import Markup
from flask_login import logout_user, login_user
from flask_login import *
from flask_login import login_required
# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()),
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        # logs registration in log file
        logging.warning('SECURITY - Register [%s, %s]',
                        form.email.data,
                        request.remote_addr)

        # sends user to login page
        return redirect(url_for('users.login'))

    # if request method is GET or form not valid re-render signup page
    return render_template('users/register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    #creates a login form object
    form = LoginForm()

    # creates session auth attempts
    if not session.get('authentication_attempts'):
        session['authentication_attempts'] = 0

    if form.validate_on_submit():

        # gets user from database
        user = User.query.filter_by(email=form.email.data).first()

        # checks if user existed when queried and passwords match
        if not user or not bcrypt.checkpw(form.password.data.encode('utf-8'),user.password):
            logging.warning('SECURITY - Invalid Login [%s, %s]',
                            user.id,
                            request.remote_addr
                            )
            session['authentication_attempt'] += 1
            # outputs that attempts exceeded allowed limit
            if session.get('authentication_attempts') >= 3:
                flash(Markup('Number of incorrect login attempts exceeded.'
                             'Please click <a href="/reset">here</a> to reset.'))
            # outputs remaining attempts before lockout
            attempts_remaining = 3-session.get('authentication_attempts')
            flash('Please check login details and try again,'
                  '{} login attempts remaining' .format(attempts_remaining))

            render_template('users/login.html', form=form, )

        else:
            login_user(user)
            # updates login times in the users database
            user.datetime_prev_login = user.datetime_curr_login
            user.datetime_curr_login = datetime.now()
            db.session.add(user)
            db.session.commit()

            # logs login in log
            logging.warning('SECURTIY - User Login [%s, %s, %s]',
                            user.id,
                            user.username,
                            request.remote_addr
                            )

            if user.role == "admin":
                return redirect(url_for('users.profile'))
            else:
                return redirect(url_for('admin.admin'))

    return render_template('users/login.html', form=form)


# view user profile
@users_blueprint.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', name="current_user.firstname")


@users_blueprint.route('/reset')
def reset():
    session['authentication_attempts'] = 0
    return redirect(url_for('users.login'))


# view user account
@users_blueprint.route('/account')
@login_required
def account():
    return render_template('users/account.html',
                           acc_no="current_user.id",
                           email="current_user.email",
                           firstname="current_user.firstname",
                           lastname="current_user.lastname",
                           phone="current_user.phone")


@users_blueprint.route('/logout')
@login_required
def logout():
    # logs the logout in log file
    logging.warning('SECURITY - Log out [%s, %s, %s]',
                    current_user.id,
                    current_user.email,
                    request.remote_addr
                    )

    logout_user()
    return redirect(url_for('main.index'))
