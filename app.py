from flask import Flask,flash,request,redirect,url_for
from flask import render_template
from werkzeug.utils import secure_filename
from db.convert import read_excel_to_sqlite

import sqlite3
import os
from pathlib import Path


ALLOWED_EXTENSIONS = {"xls","xlsx"}
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

#app.config["DATABASE"] = "db/bookoutlet.sqlite"
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "db/uploaded/")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower()

@app.route("/", methods = ["GET","POST"])
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
            return redirect(url_for("/table"))
    return render_template("/upload.html")

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