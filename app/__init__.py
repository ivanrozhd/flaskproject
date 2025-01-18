from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
# Create the Flask app
bcrypt_ = Bcrypt()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9a7b3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database, bcrypt and login manager
    db.init_app(app)
    bcrypt_.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login' #TODO: Play around with this

    from app.routes import main
    app.register_blueprint(main)
    migrate.init_app(app, db)

    return app



