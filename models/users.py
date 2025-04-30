from db import db
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, relationship

class User(db.Model):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    uname = mapped_column(String, nullable=False, unique=True)
    # classes = relationship("Classlist", back_populates="students")