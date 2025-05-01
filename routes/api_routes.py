from flask import Blueprint, request, render_template, url_for, redirect
from datetime import datetime
from db import db
from models import Event
import re

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/add", methods=["POST"])
def add():
    # date_format = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}(AM|PM)$")
    # if request.form.get('deadline') and date_format.match(request.form.get('deadline')) and request.form.get('event'):
        # db.session.add(Event(description=request.form.get('event'), deadline=datetime.strptime(request.form.get('deadline'), '%Y-%m-%d %H:%M%p'), courseid=request.form.get('id')))
    # else:
        # db.session.add(Event(description=request.form.get('event'), courseid=request.form.get('id')))
    db.session.add(Event(description=request.form.get('event'), deadline=datetime.strptime(request.form.get('deadline')+' 11:59PM', '%Y-%m-%d %I:%M%p'), courseid=request.form.get('id')))
    db.session.commit()
    return redirect(url_for("class_page", id=request.form.get('id')))