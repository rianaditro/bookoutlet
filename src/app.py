from flask import Flask

from extensions import db,migrate,login_manager
from views import view
from view_api import api
from user_view import user,login_manager
from config import BaseConfig


def create_app():
    app = Flask(__name__)

    app.config.from_object(BaseConfig)

    from models import Book,User

    db.init_app(app=app)
    migrate.init_app(app=app,db=db)
    login_manager.init_app(app=app)

    app.register_blueprint(api)
    app.register_blueprint(user)
    app.register_blueprint(view)

    return app

if __name__=="__main__":

    app = create_app()
    app.run()