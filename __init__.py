from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .db_mssql import engine
from flask_login import LoginManager
from flask_migrate import Migrate
import os


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))

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

    # blueprint for non-auth parts of app
    from project.assistant.routes import assistant_bp
    app.register_blueprint(assistant_bp)

    # blueprint for non-auth parts of app
    from project.integrations.routes import integration_bp
    app.register_blueprint(integration_bp)

    migrate = Migrate(app, db)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)