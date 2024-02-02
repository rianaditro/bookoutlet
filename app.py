from flask import Flask
from flask import render_template
from db.convert import read_excel_to_html

app = Flask(__name__)

@app.route("/")
def home():
    html = read_excel_to_html("final_result.xlsx")
    return render_template("/index.html",html=html)

@app.route("/hallo")
def hallo():
    return "hallo"

if __name__=="__main__":
    app.run(debug=True)