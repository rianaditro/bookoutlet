from flask import Flask
from pathlib import Path

from manage_db.extensions import db,migrate
from views import view

import os


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = f"{BASE_DIR}/managed_db/uploaded"


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///old.sqlite"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config["DEBUG"] = True

    from manage_db.models import Book

    db.init_app(app=app)
    migrate.init_app(app=app,db=db)

    app.register_blueprint(view)

    return app

if __name__=="__main__":
    app = create_app()
    app.run()