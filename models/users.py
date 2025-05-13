from db import db
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    uname = mapped_column(String, nullable=False, unique=True)
    passwd = mapped_column(String, nullable=False)