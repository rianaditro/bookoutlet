import os

from flask import Blueprint, render_template

from ext import db


scraper = Blueprint("scraper", __name__)

@scraper.route("/")
def index():
    return render_template("app.html")