from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from app.config import Configure
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS
import os

environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get('SCHEMA')
def add_prefix_for_prod(attr):
    if environment == "production":
        return f"{SCHEMA}.{attr}"
    else:
        return attr

app = Flask(__name__, static_folder='../react-cap/build', static_url_path='/')
app.config.from_object(Configure)
db = SQLAlchemy(app)
Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'users.unauthorized'
CORS(app)

from app.models import User
from app.forms import LoginForm
from app.routes import user_routes
from app.routes import gamer_routes
from app.routes import trade_routes
from app.routes import review_routes


@app.before_request
def https_redirect():
    if os.environ.get('FLASK_ENV') == 'production':
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)



@login_manager.user_loader
def load_user(id):
    # id = str(id).encode('utf-8')
    return User.query.get(id)


from app.seeders import seeder_command
app.cli.add_command(seeder_command)


app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(gamer_routes, url_prefix='/api/gamers')
app.register_blueprint(trade_routes, url_prefix='/api/trades')
app.register_blueprint(review_routes, url_prefix='/api/reviews')


@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        secure=True if os.environ.get('FLASK_ENV') == 'production' else False,
        samesite='Strict' if os.environ.get(
            'FLASK_ENV') == 'production' else None,
        httponly=True)
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    if path == 'favicon.ico':
        return app.send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')
