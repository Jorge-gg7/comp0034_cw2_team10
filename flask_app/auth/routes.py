from sqlalchemy.exc import IntegrityError

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, login_required, logout_user, current_user
from flask_app.auth.forms import LoginForm

from datetime import timedelta

from urllib.parse import urlparse, urljoin

from flask_app import db, login_manager
from flask_app.auth.forms import SignupForm
from flask_app.models import User

auth_bp = Blueprint('auth_bp', __name__)


@login_manager.user_loader
def load_user(user):
    """ Takes a user ID and returns a user object or None if the user does not exist"""
    if user is not None:
        return User.query.get(user)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        login_user(user, remember=login_form.remember.data, duration=timedelta(minutes=1))
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main_bp.home'))
    return render_template('login.html', title='Login', form=login_form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Welcome, {user.first_name} {user.last_name}.")
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('auth_bp.signup'))
        return redirect(url_for('main_bp.home'))
    return render_template('signup.html', title='Sign Up', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.home'))
