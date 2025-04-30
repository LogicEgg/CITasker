from db import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship

class Course(db.Model):
    __tablename__ = "courses"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    term = mapped_column(Integer, nullable=False)
    # events = relationship("Event")
    # class_list = relationship("Classlist", back_populates="course")