from db import db
from app import app
import sys
import csv
import os
from models import Course, User, Event

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

def sample_events():
    db.session.add(Event(description="Some event.", courseid=1, userid=1))
    db.session.commit()

def fake_user():
    alice = User(uname="Alice")
    bob = User(uname="Bob")
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
            print("You need to provide at least 1 command.")