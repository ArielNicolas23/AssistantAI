from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .db_mssql import engine
from flask_login import LoginManager
from flask_migrate import Migrate
import os


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))
# TOKEN = os.environ["META_TOKEN"]
# IGTOKEN = os.environ["IG_TOKEN"]
# METACLIENTID = os.environ["META_CLIENT_ID"]
# METASECRET = os.environ["META_SECRET"] 
# IGCLIENTID = os.environ["IG_CLIENT_ID"]
# IGSECRET = os.environ["IG_SECRET"]

#Temp
TOKEN = 'Prueba'
IGTOKEN = 'Prueba'
METACLIENTID = '393577946782429'
METASECRET = '9f55bd11b125a464babf8cba2b99ff87'
IGCLIENTID = '443897407962766'
IGSECRET = '150c1f837d665954a955966e53137060'
ACCESS_TOKEN = '393577946782429|Wb9-Tg4nJdKGNJotqoXOxxJPrKQ'


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from project.auths.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # blueprint for assistant of app
    from project.assistant.routes import assistant_bp
    app.register_blueprint(assistant_bp)

    # blueprint for integration module of app
    from project.integrations.routes import integration_bp
    app.register_blueprint(integration_bp)

    # blueprint for webhook app
    from project.webhooks.routes import webhook_bp
    app.register_blueprint(webhook_bp)

    migrate = Migrate(app, db)
    return app



if __name__ == "__main__": 
    app = create_app()