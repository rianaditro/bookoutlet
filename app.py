from flask import Flask,flash,request,redirect,url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.utils import secure_filename
#from db.convert import read_excel_to_sqlite

import sqlite3
import os,math
from pathlib import Path


ALLOWED_EXTENSIONS = {"xls","xlsx"}
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR}/bookoutlet.sqlite'

db = SQLAlchemy(app)

app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "db/uploaded/")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower()

class Book(db.Model):
    __table__ = "bookTable"
    title:Mapped[str]
    author:Mapped[str]
    price:Mapped[float]
    binding:Mapped[str]
    isbn:Mapped[int] = mapped_column(primary_key=True)
    publisher_date = Mapped[str]
    publisher = Mapped[str]
    language = Mapped[str]
    page_count = Mapped[int]
    dimension = Mapped[str]
    image = Mapped[str]
    

#raise Exception(db.metadata.tables)

@app.route("/another", methods = ["GET","POST"])
def upload_excel():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = app.config["UPLOAD_FOLDER"]
            file.save(save_path+filename)
            #read_excel_to_sqlite(file)
            return redirect(url_for("table"))
    return render_template("/upload.html")

def read_db():
    sql_query = text("SELECT * FROM bookTable")
    data = db.paginate(sql_query)
    return data

@app.route("/")
def table():
    #page = request.args.get('page',1)
    data = db.paginate(db.select(Book))

    return render_template("/table.html", data = data)

# @app.route("/")
# def index():
#     page = request.args.get('page', 1, type=int)
#     per_page = 20  # Number of items per page

#     book = Book.query.paginate(page=page, per_page=per_page)

#     return render_template('index.html', books=book)

if __name__=="__main__":
    app.run(debug=True)