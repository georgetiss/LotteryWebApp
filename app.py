# IMPORTS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_talisman import Talisman
import logging

"""
# configure a logger
class SecurityFilter(logging.Filter):
    def filter(self, record):
        return 'SECURITY' in record.getMessage()


logger = logging.getLogger()
file_handler = logging.FileHandler('lottery.log', 'a')
file_handler.addFilter(SecurityFilter())
formatter = logging.Formatter('%(asctime)s : %(message)s', '%m/%d/%Y %I:%M:%S %p')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
"""
# load .env
load_dotenv()

# CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')


# initialise database
db = SQLAlchemy(app)

# sets up talisman for HTTP security headers
csp = {
    'default-src': [
        '\'self\'',
        'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css'
    ],
    'frame-src': [
        '\'self\'',
        'https://www.google.com/recaptcha/',
        'https://recaptcha.google.com/recaptcha/'
    ],
    'script-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'https://www.google.com/recaptcha/',
        'https://www.gstatic.com/recaptcha/'
    ]

}
talisman = Talisman(app, content_security_policy=csp)
talisman.strict_transport_security = False

# load env
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('main/index.html')


# BLUEPRINTS
# import blueprints
from users.views import users_blueprint
from admin.views import admin_blueprint
from lottery.views import lottery_blueprint


# # register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(lottery_blueprint)

# instance of Loginmanager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# error handling
@app.errorhandler(400)
def bad_request(error):
    return render_template("errors/400.html"), 400


@app.errorhandler(403)
def page_forbidden(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500


@app.errorhandler(503)
def service_unavailable(error):
    return render_template("errors/503.html"), 503


if __name__ == "__main__":
    app.run()
