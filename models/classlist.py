from db import db
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, relationship

class Classlist(db.Model):
    __tablename__ = "classlists"

    id = mapped_column(Integer, primary_key=True)
    # course = relationship("Course", back_populates="classlist")
    # students = relationship("User", back_populates="classes")