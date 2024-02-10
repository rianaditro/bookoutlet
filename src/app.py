from flask import Flask
from pathlib import Path

from extensions import db,migrate,login_manager
from views import view
from view_api import api
from view_login import login_user

import os


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = f"{BASE_DIR}/managed_db/uploaded"


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///old.sqlite"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config["DEBUG"] = True

    from models import Book,User

    db.init_app(app=app)
    migrate.init_app(app=app,db=db)
    login_manager.init_app(app=app)

    app.register_blueprint(api)
    app.register_blueprint(login_user)
    app.register_blueprint(view)

    return app

if __name__=="__main__":
    app = create_app()
    app.run()