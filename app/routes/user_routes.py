from flask import Blueprint, render_template, request
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, SignupForm
from app import db
from app.models import User
from app.routes.gamer_routes import format_form_errors

user_routes = Blueprint('users', __name__)


@user_routes.route('/auth')
def check_user():
    if current_user.is_authenticated:
        return current_user.format_dict()
    return {'errors': ['Must be logged in.']}


@user_routes.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.data['credential']).first()
        if not user:
            user = User.query.filter(User.email == form.data['credential']).first()
            if not user:
                return {'errors': ['User does not exist.']}
        login_user(user)
        return user.format_dict()
    return {'errors': format_form_errors(form.errors)}


@user_routes.route('/signup', methods=['POST'])
def sign_up():
    form = SignupForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return user.format_dict()
    return {'errors': format_form_errors(form.errors)}


@user_routes.route('/logout')
def logout():
    logout_user()
    return {'message': 'User logged out'}


@user_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': ['Unauthorized']}, 401
