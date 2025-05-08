from flask import Blueprint, request, render_template, url_for, redirect, jsonify
from datetime import datetime
from db import db
from models import Event, Course
from sqlalchemy import select

import re

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/add", methods=["POST"])
def add():
    # date_format = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}(AM|PM)$")
    # if request.form.get('deadline') and date_format.match(request.form.get('deadline')) and request.form.get('event'):
        # db.session.add(Event(description=request.form.get('event'), deadline=datetime.strptime(request.form.get('deadline'), '%Y-%m-%d %H:%M%p'), courseid=request.form.get('id')))
    # else:
        # db.session.add(Event(description=request.form.get('event'), courseid=request.form.get('id')))
    date_format = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
    string_check = lambda event: type(event) is str and event != ""
    date_check = lambda deadline: date_format.match(deadline)
    int_check = lambda id: id.isnumeric()
    if string_check(request.form.get('event')) and date_check(request.form.get('deadline')) and int_check(request.form.get('id')):
        db.session.add(Event(description=request.form.get('event'), deadline=datetime.strptime(request.form.get('deadline')+' 11:59PM', '%Y-%m-%d %I:%M%p'), courseid=request.form.get('id')))
        db.session.commit()
        return redirect(url_for("class_page", id=request.form.get('id')))
    else:
        return {"message": "Bad data"}, 400

@api_bp.route("/edit/<int:eventid>", methods=["POST"])
def edit(eventid):
    if request.form.get('_method') == 'PUT':
        to_edit = db.session.execute(select(Event).where(Event.id == eventid)).scalar()
        updated_data = request.form
        if updated_data.get('event'):
            to_edit.description = updated_data.get('event')
        if updated_data.get('deadline'):
            to_edit.deadline = datetime.strptime(updated_data.get('deadline')+' 11:59PM', '%Y-%m-%d %I:%M%p')
        db.session.commit()
        course = db.session.execute(select(Course).where(Course.id == to_edit.courseid)).scalar()
        return redirect(url_for("class_page", id=course.id))
    else:
        return jsonify({"message": "Nice try."})
    
@api_bp.route("/delete/<int:eventid>", methods=["POST"])
def delete(eventid):
    if request.form.get('_method') == 'DELETE':
        del_tgt = db.session.execute(select(Event).where(Event.id == eventid)).scalar()
        if del_tgt:
            id_redirect = del_tgt.courseid
            db.session.delete(del_tgt)
            db.session.commit()
            return redirect(url_for('class_page', id=id_redirect))
    else:
        return jsonify({"message": "Failed to delete."})