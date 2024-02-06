from flask import Blueprint, render_template

from manage_db.extensions import db


view = Blueprint("view",__name__)

@view.route("/")
def index():
    return render_template("index.html")

@view.route("/table")
def table():
    return render_template()