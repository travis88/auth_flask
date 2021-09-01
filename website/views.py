from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import db, Note

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        data = request.form["note"]
        new_note = Note(data=data, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()

    return render_template("home.html", user=current_user)
