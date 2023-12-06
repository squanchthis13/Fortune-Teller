'''
Modified 28Nov23

@author: chelseanieves
'''

import logging
import socket
from os import path
import sqlite3
import hashlib
import uuid
import string

# create logger name and object
logger = logging.getLogger(__name__)
LOG_NAME = "./log.txt"
SPECIAL_CHAR = string.punctuation # special characters to validate password requirements
COMMON_PASS = 'filepath/' # MODIFY WITH ACTUAL PATHNAME WHEN PROGRAM IS FUNCTIONAL

#REFERENCE https://docs.python.org/3/library/sqlite3.html

# Create a new database and open a database connection
DB_NAME = "fortuneteller.db"

def create_table():
    ''' Creates 3 SQL tables to store user and previous fortune data ''' 
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor() 
    # create table USER
    query1 = "CREATE TABLE IF NOT EXISTS user(userId VARCHAR NOT NULL PRIMARY KEY, first_name TEXT, last_name TEXT, password VARCHAR, salt)"
    # create table FORTUNE
    query2 = "CREATE TABLE IF NOT EXISTS fortune(fortuneId INTEGER PRIMARY KEY AUTOINCREMENT, category VARCHAR)"
    # create bridge table TRANSACTION
    #query3 = "CREATE TABLE IF NOT EXISTS transaction(username VARCHAR, fortuneId INTEGER, FOREIGN KEY(username) REFERENCES user(username), FOREIGN KEY(fortuneId) REFERENCES fortune(fortuneId)"

    # execute table creation queries
    cur.execute(query1)
    cur.execute(query2)
    #cur.execute(query3)
    # commit changes
    con.commit()
    # close DB curser
    cur.close()
    #close DB connection
    con.close()

def sign_up(uname, fname, lname, pass1, pass2):
    '''Accepts input from tkinter labels
    Validates username does not already exist in DB
    Confirms desired password matches password confirmation field
    Commits user data to db if valid'''

    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()
    
    username = uname.lower().strip()
    fname = fname.lower().strip()
    lname = lname.lower().strip()
    
    # Program is totally skipping over the if statements, validate_pass() is never called
    if check_exists(username):
        # call method to query database by username to determine if username is already registered
        print("Username unavailable")
    elif uname == "" or pass1 == "" or pass2 == "":
        #Fields cannot be left blank
        print("Field cannot be left blank.")
    elif validate_pass(pass1, pass2) is True:
        #Username not already in DB
        #Desired pass and confirmation pass match
        #Fields are not left blank
        # Adding salt at the last of the password
        salt = uuid.uuid4().hex
        hashed_pass = hashlib.sha512(pass1.encode()).hexdigest()
        password = hashed_pass + salt
        cur.execute("INSERT INTO user (userId, first_name, last_name, password, salt) VALUES (?, ?, ?, ?, ?)", (username, fname, lname, password, salt))
        con.commit() #Commit the transaction
    
    # NEW NEW NEW
    # Nieves, Chelsea 30Nov
    # output SQL table in console for troubleshooting purposes
    # CAN BE DELETED LATER    
    readSqliteTable()
    
    # close DB curser
    cur.close()
    #close DB connection
    con.close()

 # NEW NEW NEW
 # Nieves, Chelsea 30 Nov
def check_exists(username):
    ''' method to check if username already exists in db'''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()
    query = 'SELECT userId FROM user WHERE userId = ?', 
    res = cur.execute('SELECT userId FROM user WHERE userId=?', (username,))
    data = res.fetchall()
    if len(data) != 0:
        # username exists in db
        return True
    else:
        # username does not exist in db
        return False
    # close DB curser
    cur.close()
    #close DB connection
    con.close()

# NEW NEW NEW
# Nieves, Chelsea 30 Nov
# Temporary method to display table data and ensure user data is appropriately appended to db
# CAN BE DELETED LATER
def readSqliteTable():
    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from user"""
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("Username: ", row[0])
            print("First: ", row[1])
            print("Last: ", row[2])
            print("Hashed Pass: ", row[3])
            print("Salt: ", row[4])
            print("\n")

        cur.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")

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
        # file not found error
        print("Could not find file CommonPassword.txt")
        return False

def display_previous_fortunes():
    '''Displays previous fortunes to authenticated user'''
    # username is PK so should be able to just query by that and list all

def auth_user():
    '''Authenticates user'''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()
    
    #VALIDATE INPUT
    #if input is valid, query db
    
    #query salt from db
    salt = cur.execute('SELECT salt FROM user WHERE username = ?', (uname))
    
    #hash and salt supplied pass for comparison
    hashed_pass = hashlib.sha512(password+salt).hexdigest()
    
    #query db for username and pass matching uname and hashed_pass
    cur.execute('SELECT * FROM user WHERE username = ? AND password = ?', (uname, hashed_pass))
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