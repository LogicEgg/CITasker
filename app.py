from flask import Flask, render_template
from flask_login import current_user, login_required
from pathlib import Path
from config import SECRET_KEY
from db import db
from sqlalchemy import select, and_
from models import Course, Event
from routes import api_bp, auth_bp, login_manager
from datetime import datetime, timedelta
import operator

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.config["SECRET_KEY"] = SECRET_KEY
app.instance_path = Path(".").resolve()

app.register_blueprint(api_bp)
app.register_blueprint(auth_bp)

login_manager.init_app(app)

db.init_app(app)

@app.route("/")
@login_required
def homepage():
    urgent = [i for i in db.session.execute(select(Event).where(and_(Event.deadline < datetime.now() + timedelta(days=4), Event.completed == False, Event.userid == current_user.id))).scalars()]
    urgent.sort(key=operator.attrgetter('deadline'))
    complete = [i for i in db.session.execute(select(Event).where(and_(Event.completed, Event.userid == current_user.id))).scalars()]
    events = [i for i in db.session.execute(select(Event).where(and_(Event.userid == current_user.id))).scalars()]
    due = [i for i in db.session.execute(select(Event).where(and_(Event.deadline > datetime.now(), Event.deadline < (datetime.now() + timedelta(days=1)), Event.completed == False, Event.userid == current_user.id))).scalars()]
    overdue = [i for i in db.session.execute(select(Event).where(and_(Event.deadline < datetime.now(), Event.completed == False, Event.userid == current_user.id))).scalars()]
    completion_percentage = 100
    if len(events) > 0:
        completion_percentage = round(len(complete)/len(events)*100)
    return render_template("index.html", upcoming=urgent, user=current_user, completed=complete, today=due, overdue=overdue, percent=completion_percentage)

@app.route("/terms")
def term_page():
    return render_template("terms.html")

@app.route("/terms/<int:num>")
def term_classes(num):
    data = db.session.execute(select(Course).where(Course.term == num)).scalars()
    return render_template("classes.html", data=data, num=num)

@app.route("/classes/<int:id>", methods=["GET"])
@login_required
def class_page(id):
    course = db.session.execute(select(Course).where(Course.id == id)).scalar()
    events = [i for i in db.session.execute(select(Event).where(and_(Event.courseid == id, Event.userid == current_user.id))).scalars()]
    events.sort(key=operator.attrgetter('deadline'))
    return render_template("class_page.html", course=course, events=events, user=current_user)

if __name__ == "__main__":
    app.run(debug=True, port=3000)