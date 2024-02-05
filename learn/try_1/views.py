from flask import Blueprint, render_template,redirect,url_for


scraper = Blueprint("scraper",__name__)

@scraper.route("/")
def index():
    return render_template("index.html")

@scraper.route("/next")
def next():
    return render_template("next.html")

@scraper.route("/homepage")
def homepage():
    return redirect(url_for('scraper.index'))