from os import path
from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# Create the database instance
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app(config_filename='config.py'):
    app = Flask(__name__)

    # Application configuration
    app.config['SECRET_KEY'] = "dsakfhaosjbdjvbakshefkdsafaseh"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"  # Configure the database URI
    db.init_app(app)  # Initialize the database with the app

    # Initialize Flask-Login (after app and db initialization)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # Set the login view endpoint
    login_manager.init_app(app)

    # Register Blueprints (now safe to import)
    from app.auth import auth  # Import the auth Blueprint here to avoid circular imports
    app.register_blueprint(auth, url_prefix='/auth')  # Register auth blueprint

    # Initialize Flask-RESTful API
    api = Api(app)

    # Create database if it doesn't exist
    create_database(app)

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    return app


def create_database(app):
    with app.app_context():
        # Check if the database exists, if not, create it
        if not path.exists(f"app/{DB_NAME}"):
            db.create_all()
            print("Created Database Successfully!")
