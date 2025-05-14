from db import db
from app import app
import sys
import csv
import os
from models import Course, User, Event
from pathlib import Path
import hashlib
from config import pass1, pass2, SALT
from sqlalchemy import select

def create():
    db.create_all()
    print("Tables created.")

def drop():
    db.drop_all()
    print("Tables dropped.")

def classes_file(csvfile):
    with open(csvfile) as classes:
        data = csv.DictReader(classes)
        for line in data:
            db.session.add(Course(name=line["coursename"], term=int(line["term"])))
        db.session.commit()
    print("Classes added.")

def sample_events(description="Some Event", course=1, user=1):
    if type(description) != str or type(course) != int:
        raise ValueError("Invalid data type")
    db.session.add(Event(description=description, courseid=course, userid=user))
    db.session.commit()

def kill_event(description):
    if type(description) != str:
        raise ValueError("Description should be a string")
    target = db.session.execute(select(Event).where(Event.description == description)).scalar()
    if not target:
        return "Event not found"
    else:
        db.session.delete(target)
        db.session.commit()
        return "Event killed"

def fake_user():
    alice = User(uname="Alice", passwd=str(hashlib.sha256((pass1+SALT).encode()).hexdigest()))
    bob = User(uname="Bob", passwd=str(hashlib.sha256((pass2+SALT).encode()).hexdigest()))
    db.session.add(alice)
    db.session.add(bob)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        coms = {
            "create": create,
            "drop": drop,
            "add_usrs": fake_user,
            "add_classes": classes_file,
            "add_events": sample_events
            }

        if len(sys.argv) > 1:
            for command in sys.argv[1:]:
                if "add_classes" in command and command.split("-")[1] in os.listdir(os.getcwd()):
                    coms["add_classes"](command.split("-")[1])
                elif command in coms:
                    coms[command]()
                else:
                    print(f"Available commands are {coms.keys()}")
        else:
            if "events.db" not in os.listdir(Path(".").resolve()):
                create()
                fake_user()
                classes_file()