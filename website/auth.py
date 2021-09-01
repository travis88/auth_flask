from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/sign_up", methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists.", category="danger")
        elif len(email) < 5:
            flash("Email must be greater than 4 characters.", category="danger")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="danger")
        elif password != password_confirmation:
            flash("Password don't match.", category="danger")
        elif len(password) < 7:
            flash("Password must be at least 7 characters.", category="danger")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))
    
    return render_template("sign_up.html", user=current_user)

@auth.route("/login", methods=["GET","POST"])    
def login():
    if request.method == "POST":
        data = request.form
        email = data["email"]
        password = data["password"]

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="danger")
        else:
            flash("Email does not exists.", category="danger")

    return render_template("login.html", user=current_user)

@auth.route("/logout")    
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
