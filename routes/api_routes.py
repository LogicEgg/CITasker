from flask import Blueprint, request, render_template, url_for, redirect
from datetime import datetime
from db import db
from models import Event

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/add", methods=["POST"])
def add():
    db.session.add(Event(description=request.form.get('event'), deadline=datetime.strptime(request.form.get('deadline'), '%Y-%m-%d %H:%M%p'), courseid=request.form.get('id')))
    db.session.commit()
    return redirect(url_for("class_page", id=request.form.get('id')))