from flask import request,redirect,render_template,flash,url_for
from werkzeug.utils import secure_filename
from pathlib import Path


ALLOWED_EXTENSIONS = {"xls","xlsx"}
BASE_DIR = Path(__file__).resolve().parent


def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower()    

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

