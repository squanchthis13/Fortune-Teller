
'''
Modified 27Nov23

@author: chelseanieves
'''

import logging
import socket
from os import path
import sqlite3
import hashlib
import uuid

# create logger name and object
logger = logging.getLogger(__name__)
LOG_NAME = "./log.txt"

#REFERENCE https://docs.python.org/3/library/sqlite3.html

#First, we need to create a new database and open a database connection to allow sqlite3 to work
#with it. Call sqlite3.connect() to create a connection to the database tutorial.db in the current
#working directory, implicitly creating it if it does not exist
DB_Name = "Test.db"
con = sqlite3.connect(DB_NAME)
#In order to execute SQL statements and fetch results from SQL queries, we will need to use a 
#database cursor. Call con.cursor() to create the Cursor:
cur = con.cursor() 

cur.execute("CREATE TABLE user(userid, username, password, salt)")

data = [
    (1, "test user", "hashed password", "salt stored to be able to reauth user"),
    (2, "test user 2", "pass", "salt"),
]

cur.executemany("INSERT INTO user VALUES (?, ?, ?)", data)
con.commit() #Commit the transaction

#view table data
for row in cur.execute("SELECT username FROM user ORDER BY userid"):
    print(row)

# REFERENCE https://www.geeksforgeeks.org/how-to-get-the-tkinter-label-text/#
import tkinter as tk
master = tk.Tk()
master.configure(bg='light grey') 
l = tk.Label(master,
            text="Placeholder label for sign up func")

def sign_up():
## I think I forgot to salt the password actually so we will need to do that possibly and store the salt as well?
        
        uname = c.get("text")
        #Desired password
        pass1 = c.get("text")
        #Confirm password
        pass2 = c.get("text")
        # query database by username to determine if  user is already registered
        res = cur.execute("SELECT username FROM sqlite_master WHERE username='uname'")

        if res.fetchone() is None == False:
            #If username is found in the db
            print("Invalid username or password, please try again")
        elif uname == "" or pass1 == "" or pass2 == "":
            #Fields cannot be left blank
            print("Field cannot be left blank.")
        elif validate_pass(password1, password2) is True:
            #Username not already in DB
            #Desired pass and confirmation pass match
            #Fields are not left blank
            password = generate_password_hash(pass1, method= "sha256")
            salt = uuid.uuid4().hex
            hashed_pass = hashlib.sha512(password+salt).hexdigest()
            data = [
                (1, uname, hashed_password, salt),
                ]
            cur.executemany("INSERT INTO user VALUES (?, ?, ?)", data)
            con.commit() #Commit the transaction

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
                #Password is valid
                return True
    except IOError:
        print("Could not find file CommonPassword.txt")
        return False

def auth_user():
    

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



