from flask import Flask, render_template, request
from pathlib import Path
from db import db
from sqlalchemy import select
from models import Course, Event
from routes import api_bp
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.instance_path = Path(".").resolve()

app.register_blueprint(api_bp)

db.init_app(app)


@app.route("/")
def homepage():
    urgent = db.session.execute(select(Event).where(Event.deadline < datetime.now() + timedelta(days=4))).scalars()
    return render_template("index.html", upcoming=urgent)


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
    events = db.session.execute(select(Event).where(Event.courseid == id)).scalars()
    return render_template("class_page.html", course=course, events=events)


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
