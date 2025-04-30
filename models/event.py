from db import db
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, relationship
from datetime import datetime, timedelta

class Event(db.Model):
    __tablename__ = "events"

    id = mapped_column(Integer, primary_key=True)
    userid = mapped_column(Integer, ForeignKey("users.id"))
    description = mapped_column(String, nullable=False)
    deadline = mapped_column(DateTime, default=datetime.now() + timedelta(days=1))
    courseid = mapped_column(Integer, ForeignKey("courses.id"))
    # course = relationship("Course", back_populates="events")