
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
import string
import tkinter as tk

# create logger name and object
logger = logging.getLogger(__name__)
LOG_NAME = "./log.txt"
SPECIAL_CHAR = string.punctuation
COMMON_PASS = 'filepath/'

#REFERENCE https://docs.python.org/3/library/sqlite3.html

# Create a new database and open a database connection
DB_NAME = "fortuneteller.db"

def create_table():
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor() 
    query1 = "CREATE TABLE user(username VARCHAR NOT NULL PRIMARY KEY, email VARCHAR NOT NULL UNIQUE, password VARCHAR, salt)"   
    query2 = "CREATE TABLE fortune(fortuneId INTEGER PRIMARY KEY AUTOINCREMENT, category VARCHAR)"
    query3 = "CREATE TABLE transaction(username VARCHAR, fortuneId INTEGER, FOREIGN KEY(username) REFERENCES user(username), FOREIGN KEY(fortuneId) REFERENCES fortune(fortuneId)"
                     
    cur.execute(query1)
    cur.execute(query2)
    cur.execute(query3)
    # commit changes
    cur.commit()
    # close DB curser
    cur.close()
    #close DB connection
    con.close()

def sign_up(uname, pass1, pass2):
    '''Accepts input from tkinter labels
    Validates username does not already exist in DB
    Confirms desired password matches password confirmation field
    Commits user data to db if valid'''

    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor() 
    
    # uname = l.cget("text")
    # #Desired password
    # pass1 = l.cget("text")
    # #Confirm password
    # pass2 = l.cget("text")
    
    # query database by username to determine if  user is already registered
    res = cur.execute("SELECT username FROM sqlite_master WHERE username='uname'")
    data = res.fetchall()
    
    if len(data) != 0:
        #If username is found in the db
        print("Invalid username or password, please try again")
    elif uname == "" or pass1 == "" or pass2 == "":
        #Fields cannot be left blank
        print("Field cannot be left blank.")
    elif validate_pass(pass1, pass2) is True:
        #Username not already in DB
        #Desired pass and confirmation pass match
        #Fields are not left blank
        salt = uuid.uuid4().hex
        hashed_pass = hashlib.sha512(pass1+salt).hexdigest()
        cur.execute("INSERT INTO user VALUES (?, ?, ?)", (uname, hashed_pass, salt))
        con.commit() #Commit the transaction
    # close DB curser
    cur.close()
    #close DB connection
    con.close()

def validate_pass(password1, password2):
    '''Validates user's desired password is not found in list of common passphrases.
    Validates user's desired password against requirements (12 char in length, 1 upper, 1 lower,
    1 special char)
    Returns true if user's password meets requirements.'''
    try:
        with open('CommonPassword.txt', encoding='UTF-8') as f:
            contents = f.read()
            if password1 in contents:
                #if password found in list of common passwords
                print("Error: Found in list of common passwords. Please try again.")
            elif len(password1) < 12:
                #if password length is not 12 char
                print("Invalid length: Password must be greater than 12 characters.")
            elif not any(char.isdigit() for char in password1):
                #if password does not contain at least one numerical char
                print("Error: Password must contain at least one numerical character.")
            elif not any(char.islower() for char in password1):
                #if password does not contain at least one lowercase char
                print("Error: Password must contain at least one lowercase character.")
            elif not any(char.isupper() for char in password1):
                #if password does not contain at least one uppercase char
                print("Error: Password must contain at least one uppercase character.")
            elif not any(char in SPECIAL_CHAR for char in password1):
                #if password does not contain at least one special char
                print("Error: Password must contain at least one special character.")
            elif password1 != password2:
                #if desired password does not match confirmation field
                print("Error: Passwords do not match.")
            else:
                #Password is valid
                print("Valid Password")
                return True
    except IOError:
        print("Could not find file CommonPassword.txt")
        return False

def auth_user():
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()
    
    #VALIDATE INPUT
    #if input is valid, query db
    
    #query salt from db
    salt = cur.execute('SELECT salt FROM table WHERE username = ?', (uname))
    
    #hash and salt supplied pass for comparison
    hashed_pass = hashlib.sha512(password+salt).hexdigest()
    
    #query db for username and pass matching uname and hashed_pass
    cur.execute('SELECT * FROM table WHERE username = ? AND Password = ?', (uname, hashed_pass))
    res = cur.fetchall() #will return NONE if no result
    print(res)
    # if res is NONE, error
    # else authorize user
    # commit changes to DB
    con.commit()
    # close DB curser
    cur.close()
    #close DB connection
    con.close()

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
    
CUR.close()
CON.close()
