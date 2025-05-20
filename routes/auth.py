from db import db
from flask_login import LoginManager, login_user, current_user, logout_user
from flask import Blueprint, render_template, request, redirect, url_for
from models import User
from sqlalchemy import select, and_
from .api_routes import string_check
# from config import SALT
import hashlib
from os import environ

SALT = environ.get("SALT", "123456")

login_manager = LoginManager()
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# class User(UserMixin):
#     def __init__(self, id, uname):
#         self.id = id
#         self.uname = uname

login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    
    return db.session.get(User, int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if (request.form.get('uname') and request.form.get('password')):
        user = db.session.execute(select(User).where(
            and_(User.uname == request.form.get('uname'), User.passwd == hashlib.sha256((request.form.get('password')+SALT).encode()).hexdigest()))).scalar()
        if user:
            login_user(user)
            return redirect(url_for('homepage'))
        else:
            return render_template("auth_page.html", failure=True)
    return render_template("auth_page.html", failure=False)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.form:
        if string_check(request.form.get('uname')) and string_check(request.form.get('password')) and not db.session.execute(select(User).where(User.uname == request.form.get('uname'))).scalar():
            db.session.add(User(uname=request.form.get('uname'), passwd=str(hashlib.sha256((request.form.get('password')+SALT).encode()).hexdigest())))
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return render_template("register.html", failure=True)
    return render_template("register.html", failure=False)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))