from flask import Blueprint, request, url_for, redirect
from datetime import datetime
from db import db
from models import Event, Course
from sqlalchemy import select
from flask_login import login_required

import re

api_bp = Blueprint("api", __name__, url_prefix="/api")

date_format = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
time_format = re.compile("^[0-9]{2}:[0-9]{2}$")
string_check = lambda event: type(event) is str and event != ""
date_check = lambda deadline: date_format.match(deadline)
time_check = lambda da_time: time_format.match(da_time)
int_check = lambda id: id.isnumeric()

@api_bp.route("/add", methods=["POST"])
@login_required
def add():
    # date_format = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}(AM|PM)$")
    # if request.form.get('deadline') and date_format.match(request.form.get('deadline')) and request.form.get('event'):
        # db.session.add(Event(description=request.form.get('event'), deadline=datetime.strptime(request.form.get('deadline'), '%Y-%m-%d %H:%M%p'), courseid=request.form.get('id')))
    # else:
        # db.session.add(Event(description=request.form.get('event'), courseid=request.form.get('id')))
    if string_check(request.form.get('event')) and date_check(request.form.get('deadline')) and int_check(request.form.get('id')):
        print(request.form.get('due_time'))
        db.session.add(Event(userid=request.form.get('userid'), description=request.form.get('event'), deadline=datetime.strptime(request.form.get('deadline')+f" {request.form.get('due_time')}", '%Y-%m-%d %H:%M'), courseid=request.form.get('id')))
        db.session.commit()
        return redirect(url_for("class_page", id=request.form.get('id')))
    else:
        return {"message": "Bad data"}, 400

@api_bp.route("/edit/<int:eventid>", methods=["POST"])
@login_required
def edit(eventid):
    if request.form.get('_method') == 'PUT' and db.session.execute(select(Event).where(Event.id == eventid)).scalar() and (request.form.get('event') or request.form.get('deadline')):
        to_edit = db.session.execute(select(Event).where(Event.id == eventid)).scalar()
        updated_data = request.form
        if updated_data.get('event') and string_check(updated_data.get('event')):
            to_edit.description = updated_data.get('event')
        if updated_data.get('deadline') and date_check(updated_data.get('deadline')) and time_check(updated_data.get('due_time')):
            to_edit.deadline = datetime.strptime(updated_data.get('deadline')+f" {request.form.get('due_time')}", '%Y-%m-%d %H:%M')
        db.session.commit()
        course = db.session.execute(select(Course).where(Course.id == to_edit.courseid)).scalar()
        return redirect(url_for("class_page", id=course.id))
    else:
        return {"message": "Nice try."}, 400
    
@api_bp.route("/delete/<int:eventid>", methods=["POST"])
@login_required
def delete(eventid):
    if request.form.get('_method') == 'DELETE':
        del_tgt = db.session.execute(select(Event).where(Event.id == eventid)).scalar()
        if del_tgt:
            id_redirect = del_tgt.courseid
            db.session.delete(del_tgt)
            db.session.commit()
            return redirect(url_for('class_page', id=id_redirect))
    else:
        return {"message": "Failed to delete."}, 404
    
@api_bp.route("/complete/<int:eventid>", methods=["POST"])
@login_required
def complete(eventid):
    if request.form.get('_method') == 'PUT' and db.session.execute(select(Event).where(Event.id == eventid)).scalar():
        finish = db.session.execute(select(Event).where(Event.id == eventid)).scalar()
        if not finish.completed:
            finish.completed = True
        else:
            finish.completed = False
        db.session.commit()
        class_redirect = db.session.execute(select(Course).where(Course.id == finish.courseid)).scalar()
        return redirect(url_for('class_page', id=class_redirect.id))
    else:
        return {"message": "Failed to complete."}, 400
