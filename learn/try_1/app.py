from flask import Flask
from ext import db,migrate
from views import scraper


def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bookoutlet.sqlite"

    db.init_app(app=app)
    migrate.init_app(app=app,db=db)

    app.register_blueprint(scraper)

    return app


if __name__=="__main__":
    app = create_app()
    app.run()