from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,inspect
from flask_login import LoginManager
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BeerApp.db'
    db.init_app(app)


    login_manager=LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # from .models import User
    from .models import Bars
    @login_manager.user_loader
    def load_user(id):
        return Bars.query.get(int(id))
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app