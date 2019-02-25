# app/__init__.py

# third part imports
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import os

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
# login manager initialization
login_manager = LoginManager()

def create_app(config_name):
    if os.getenv('FLASK_CONFIG') == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    # for test
    # temporary route
    # @app.route('/')
    # def hello_world():
    #    return 'Hello, World!'

    # In addition to initializing the LoginManager object, we've also added a login_view and login_message to it.
    # This way, if a user tries to access a page that they are not authorized to, it will redirect to the specified view
    # and display the specified message.
    login_manager.init_app(app)
    login_manager.login_message='You must be logged in to access this page'
    login_manager.login_view='auth.login'

    # For the auth blueprint, we'll begin by creating the registration and login forms. We'll use Flask-WTF, which will
    # allow us to create forms that are secure (thanks to CSRF protection and reCAPTCHA support).
    # % pip install Flask-WTF
    # Finally, let's work on the templates. First, we'll install Flask-Bootstrap so we can use its wtf and utils
    # libraries. The wtf library will allow us to quickly generate forms in the templates based on the forms in the
    # auth/forms/registration.py and  auth/forms/login.py file. The utils library will allow us to display the flash
    # messages we set earlier to give feedback to the user.

    # Flask Bootstrap
    # $ pip install flask-bootstrap
    Bootstrap(app)

    # Migrations allow us to manage changes we make to the models, and propagate these changes in the database.
    # For example, if later on we make a change to a field in one of the models, all we will need to do is create and
    # apply a migration, and the database will reflect the change. (pip install flask-migrate)
    # We have created a migrate object which will allow us to run migrations using Flask-Migrate. We have also imported
    # the models from the app package. Next, we'll run the following command to create a migration repository:
    # $ flask db init
    # $ flask db migrate
    # $ flask db upgrade
    migrate = Migrate(app, db)
    from app.models.employee import Employee
    from app.models.department import Department
    from app.models.role import Role

    # Blueprints
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Internal Error'), 500

    # to Test page error 500
    @app.route('/500')
    def error():
        abort(500)

    return app

    # $ set FLASK_CONFIG=development
    # $ set FLASK_APP=run.py
    # $ flask run

# We've created a function, create_app that, given a configuration name, loads the correct configuration from the
# config.py file, as well as the configurations from the instance/config.py file. We have also created a db object which
# we will use to interact with the database.