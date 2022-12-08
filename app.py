# IMPORTS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from models import User
from dotenv import load_dotenv

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

# load env
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# initialise login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('main/index.html')


# BLUEPRINTS
# import blueprints
from users.views import users_blueprint
from admin.views import admin_blueprint
from lottery.views import lottery_blueprint
from errors import errors_blueprint


# # register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(lottery_blueprint)
app.register_blueprint(errors_blueprint)


if __name__ == "__main__":
    app.run()
