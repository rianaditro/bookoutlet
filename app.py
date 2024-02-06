from flask import Flask

from manage_db.extensions import db,migrate
from views import view


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///manage_db/bookoutlet.sqlite"
    app.config["DEBUG"] = True

    from manage_db.models import Book

    db.init_app(app=app)
    migrate.init_app(app=app,db=db)

    app.register_blueprint(view)

    return app

if __name__=="__main__":
    app = create_app()
    app.run()