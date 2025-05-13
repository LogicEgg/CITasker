from flask import Flask, render_template
from pathlib import Path
from db import db
from sqlalchemy import select
from models import Course, Event
from routes import api_bp
from datetime import datetime, timedelta
import operator

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.instance_path = Path(".").resolve()

app.register_blueprint(api_bp)

db.init_app(app)

@app.route("/")
def homepage():
    events = [i for i in db.session.execute(select(Event)).scalars()]
    urgent = [i for i in db.session.execute(select(Event).where(Event.deadline < datetime.now() + timedelta(days=4))).scalars() if not i.completed]
    complete = [i for i in db.session.execute(select(Event).where(Event.completed)).scalars()]
    start = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    end = start + timedelta(1)
    due = [i for i in db.session.execute(select(Event).where(Event.deadline <= end).where(Event.deadline >= start)).scalars() if not i.completed]
    overdue = [i for i in db.session.execute(select(Event).where(Event.deadline < start)).scalars() if not i.completed]
    urgent.sort(key=operator.attrgetter('deadline'))
    completion_percentage = round(len(complete) / len(events) * 100)
    print(completion_percentage)
    return render_template("index.html", upcoming=urgent, completed=complete, today=due, overdue=overdue, percent=completion_percentage)

@app.route("/terms")
def term_page():
    return render_template("terms.html")

@app.route("/terms/<int:num>")
def term_classes(num):
    data = db.session.execute(select(Course).where(Course.term == num)).scalars()
    return render_template("classes.html", data=data, num=num)

@app.route("/classes/<int:id>", methods=["GET"])
def class_page(id):
    course = db.session.execute(select(Course).where(Course.id == id)).scalar()
    events = [i for i in db.session.execute(select(Event).where(Event.courseid == id)).scalars()]
    events.sort(key=operator.attrgetter('deadline'))
    return render_template("class_page.html", course=course, events=events)

if __name__ == "__main__":
    app.run(debug=True, port=3000)