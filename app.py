from scraping.copy_web import all_categories,open_page
from scraping.scrap_all_book_links import max_pages
from scraping.product_details import send_requests


from flask import Flask,flash,request,redirect,url_for
from flask import render_template
from werkzeug.utils import secure_filename
from db.convert import read_excel_to_sqlite

import os
from pathlib import Path


ALLOWED_EXTENSIONS = {"xls","xlsx"}
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

#app.config["DATABASE"] = "db/bookoutlet.sqlite"
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "db/uploaded/")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower()

@app.route("/")
def categories():
    link = all_categories()
    return render_template("/all_category.html",all_link = link)

@app.route("/page_category/<url>/<page>")
def category_page(url:str,page:int=1):
    url = f"{url}?page={page}"
    html = send_requests(url)
    max = max_pages(html)
    books = open_page(url)
    return render_template("/page_category.html",max = max, books = books, page = page)

@app.route("/table")
def read_db():
    """if request.method == "POST":
        f = request.files['file']
        sql_file = read_excel_to_sqlite(f)
        cursor = sql_file.execute('SELECT * FROM bookTable LIMIT 100')
        data = cursor.fetchall()
        sql_file.close()"""
    return render_template("/table.html")

@app.route("/readPandas")
def read_pandas():
    return "hallo"

if __name__=="__main__":
    app.run(debug=True)