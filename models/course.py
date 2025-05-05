from db import db
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import mapped_column, relationship
from .event import Event
import operator
from datetime import datetime

class Course(db.Model):
    __tablename__ = "courses"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    term = mapped_column(Integer, nullable=False)
    # events = relationship("Event")
    # class_list = relationship("Classlist", back_populates="course")

    def task_count(self):
        counter = [i for i in db.session.execute(select(Event).where(Event.courseid == self.id)).scalars() if not i.completed]
        return len(counter)
    
    def upcoming(self):
        next_task = [i for i in db.session.execute(select(Event).where(Event.courseid == self.id)).scalars() if not i.completed]
        next_task.sort(key=operator.attrgetter('deadline'))
        if next_task:
            return datetime.strftime(next_task[0].deadline, "%A %d, %b %Y, %I:%M%p %Z")
        else:
            return "Nothing upcoming."