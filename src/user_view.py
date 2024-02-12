from flask import Blueprint,request,redirect,url_for,render_template
from flask_login import login_user,logout_user

from extensions import db
from models import User


user = Blueprint("user",__name__)

@user.route("/sign_up",methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        if request.form:
            username = request.form.get("username")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            
            if password1 == password2:
                user = User(username=username,
                    password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("user.login",message="success"))
            else:
                return redirect(url_for("user.sign_up",message="failed"))
    return render_template("sign_up.html")

@user.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        # if no username
        if user == None:
            return redirect(url_for("user.login",message="invalid"))
        # if correct
        elif user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("view.catalog"))
        # if wrong password
        else:
            return redirect(url_for("user.login",message="invalid"))
    return render_template("login.html")

@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("view.index"))


