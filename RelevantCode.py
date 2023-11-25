
'''
Created on Jul 4, 2022

@author: chelseanieves


'''
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    '''Purpose: Creates and manages User database model'''
    '''defines database schema'''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True) # unique to prevent duplicate email entries
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
_______________________________

'''
@author 
'''

import logging
import socket
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# create logger name and object
logger = logging.getLogger(__name__)
LOG_NAME = "./log.txt"
# create database name and object
db = SQLAlchemy()
DB_NAME = "database.db"

def create_database(app):
    '''Function to validate whether a database has been created. Creates a new database
    (database.db) if it does not already exist'''
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Database created")

def create_logger():
    '''Create and modify logger'''
    # set level to log only ERROR and below
    logger.setLevel(logging.ERROR)
    # assign path to store logs
    handler = logging.FileHandler(f'{LOG_NAME}')
    # assign handler to logger
    logger.addHandler(handler)
    # getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    # getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    formatter = logging.Formatter(f'{ip_address} - %(asctime)s - %(levelname)s-%(name)s-\
    %(message)s')
    # apply formatter to logger handler
    handler.setFormatter(formatter)
    # apply filter to handler
    handler.addFilter(logger)

def sign_up():
## I think I forgot to salt the password actually so we will need to do that possibly and store the salt as well?
        
        email = request.form.get('email')
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        # query database by email to determine if  user is not already registered
        user = User.query.filter_by(email=email).first()
        if user:
            flash("There is already an account associated with this email address.",
                  category="error")
        elif email == "" or first_name == "" or password1 == "" or password2 == "":
            flash("Error: Field cannot be left blank.", category = "error")
        # password complexity should be enforced to include at least 12 characters in length,
        # and include at least 1 uppercase character, 1 lowercase character, 1 number and
        # 1 special character.
        elif validate_pass(password1, password2) is True:
            new_user = User(email=email, first_name = first_name, password =
                            generate_password_hash(password1, method= "sha256"))
            db.session.add(new_user)
            db.session.commit()

def validate_pass(password1, password2):
    '''Validates user's desired password is not found in list of common passphrases.
    Validates user's desired password against requirements (12 char in length, 1 upper, 1 lower,
    1 special char)
    Returns true if user's password meets requirements.'''
    try:
        with open(f'{COMMON_PASS}') as f:
            contents = f.read()
            if password1 in contents:
                flash("Error: Found in list of common passwords. Please try again.",
                      category = "error")
            elif len(password1) < 12:
                flash("Invalid length: Password must be greater than 12 characters.",
                      category = "error")
            elif not any(char.isdigit() for char in password1):
                flash("Error: Password must contain at least one numerical character.",
                      category = "error")
            elif not any(char.islower() for char in password1):
                flash("Error: Password must contain at least one lowercase character.",
                      category = "error")
            elif not any(char.isupper() for char in password1):
                flash("Error: Password must contain at least one uppercase character.",
                      category = "error")
            elif not any(char in SPECIAL_CHAR for char in password1):
                flash("Error: Password must contain at least one special character.",
                      category = "error")
            elif password1 != password2:
                flash("Error: Passwords do not match.", category = "error")
            else:
                return True
    except IOError:
        print("Could not find file CommonPassword.txt")
        flash("Error: Something went wrong. Unable to complete action.", category = "error")
        return False


