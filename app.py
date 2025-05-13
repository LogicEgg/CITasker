from flask import Flask, render_template
from flask_login import current_user, login_required
from pathlib import Path
from config import SECRET_KEY
from db import db
from sqlalchemy import select
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
def homepage():
    urgent = [i for i in db.session.execute(select(Event).where(Event.deadline < datetime.now() + timedelta(days=4))).scalars() if not i.completed]
    urgent.sort(key=operator.attrgetter('deadline'))
    if not current_user:
        return render_template("index.html", upcoming=urgent, user=None)
    return render_template("index.html", upcoming=urgent, user=current_user)

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
    events = [i for i in db.session.execute(select(Event).where(Event.courseid == id)).scalars()]
    events.sort(key=operator.attrgetter('deadline'))
    return render_template("class_page.html", course=course, events=events)

if __name__ == "__main__":
    app.run(debug=True, port=3000)