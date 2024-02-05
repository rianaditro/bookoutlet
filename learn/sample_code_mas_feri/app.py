from flask import Flask
from ext import db, migrate
from views import scraper

def create_app() -> Flask:
    app = Flask(__name__)

    # olah inisiasi
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bookoutlet.sqlite"
    app.config['DEBUG'] = True

    from models import Book


    # inisiasi ext
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    # register blueprint
    app.register_blueprint(scraper)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()