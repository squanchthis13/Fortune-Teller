'''
Module to create db, tables, and query/output data
'''
import sqlite3
import string
import re
from datetime import date
import tkinter as tk
from tkinter import messagebox
import bcrypt
from loghandler import user_logger, db_logger

SPECIAL_CHAR = string.punctuation  # special characters to validate password requirements
DB_NAME = 'FortuneTeller.db' # Create a new database
COMMON_PASS_PATH = 'texts/CommonPassword.txt'
is_user_logged_in = False
username = ''
#active = False # var if db has been created

def read_sqlite_table():
    '''Method to output data from User and Fortune SQLite table to console'''
    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        print('\n------------------------------------------')
        print('Connected to SQLite')

        sqlite_select_query = '''SELECT * from user'''
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
        print('Total rows are:  ', len(records))
        print('Printing each row...')
        for row in records:
            print('> Username: ', row[0])
            print('> First: ', row[1])
            print('> Last: ', row[2])
            print('> Email: ', row[3])
            print('> Hashed Pass: ', row[4])
            print('\n')

        ### NEW NEW NEW
        # display records in Fortune table
        sqlite_select_query = '''SELECT * from FORTUNE'''
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
        print('FORTUNE: ')
        print('Total rows are:  ', len(records))
        print('Printing each row...')
        for row in records:
            print('> FortuneId: ', row[0])
            print('> UserId: ', row[1])
            print('> Date: ', row[2])
            print('> Message: ', row[3])
            print('> Category: ', row[4])
            print('\n')
        cur.close()
    except sqlite3.Error as err:
        db_logger.error(err)
    finally:
        if con:
            con.close()
            print('The SQLite connection is closed')
            print('------------------------------------------')

def create_table():
    ''' Creates SQL tables to store user and previous fortune data '''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()
    try:
        cur.executescript('''
        CREATE TABLE IF NOT EXISTS user(userId VARCHAR(20) NOT NULL PRIMARY KEY, first_name TEXT(20) NOT NULL, last_name TEXT(20) NOT NULL, email VARCHAR(50) NOT NULL UNIQUE, password BLOB);
        CREATE TABLE IF NOT EXISTS fortune(fortuneId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, userId VARCHAR(20) NOT NULL, save_date TEXT, message TEXT, category VARCHAR(10) NOT NULL, FOREIGN KEY (userId) REFERENCES user(userId));
        ''')
        # commit to db
        con.commit()
        # display tables to console
        read_sqlite_table()
    except sqlite3.Error as err:
        # log db error
        db_logger.error(err)
    finally:
        if con:
            # close DB cursor
            cur.close()
            # close db connection
            con.close()

def validate_username(uname):
    '''Method to validate input username
    :return: True if valid, else false'''
    while True:
        if uname == '':
            print('ERROR: Field cannot be left blank')
            break
        if any(char in SPECIAL_CHAR for char in uname):
            print('ERROR: Field may not contain special characters.')
            break
        if len(uname) > 20:
            print('ERROR: Length may not exceed 20 characters.')
            break
        else:
            #input is valid
            print(f'INFO: {uname} is valid')
            return True
    #strng is invalid
    return False 


def validate_name(name):
    '''Method to validate input fname, lname
    :return: True if valid, else false'''
    while True:
        if name == '':
            print('ERROR: Field cannot be left blank')
            break
        if any(char in SPECIAL_CHAR for char in name):
            print('ERROR: Field may not contain special characters.')
            break
        ###NEW NEW NEW 9 DEC NIEVES,CHELSEA###
        if any(char.isdigit() for char in name):
            print('ERROR: Field may not contain any numerical characters.')
            break
        if len(name) > 20:
            print('ERROR: Length may not exceed 20 characters.')
            break
        else:
            #input is valid
            print(f'INFO: {name} is valid')
            return True
    #strng is invalid
    return False

def check_username_exists(input_username):
    '''Method to check if username already exists in db
    :return: boolean True if exists, else False
    '''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()
    # validate user input before querying db
    if validate_username(input_username):
        try:
            res = cur.execute('SELECT userId FROM user WHERE userId=?', (input_username,))
            data = res.fetchall()
            con.commit()
            if len(data) != 0:
                # username exists in db
                return True
        except sqlite3.Error as err:
            # log db error
            db_logger.error(err)
        finally:
            if con:
                # close DB cursor
                cur.close()
                # close db connection
                con.close()
    return False

# Valerie Rudich 12/5/2023
# Chelsea Nieves 7 Dec 23 modified return statements
def validate_email(email):
    '''Validates user's email address
    :return: True if valid, else false'''
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    while True:
        if email == '':
            print('Error: Email cannot be blank')
            break
        if re.match(email_regex, email):
            # email is valid
            return True
    return False

def check_email_exists(email):
    '''Method to check if email already exists in db
    :return: boolean True if exists, else False
    '''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()
    # if email is valid
    if validate_email(email):
        try:
            #query db for email
            res = cur.execute('SELECT email FROM user WHERE email=?', (email,))
            data = res.fetchall()
            con.commit()
            # if results in data
            if len(data) != 0:
                # email exists in db
                return True
        except sqlite3.Error as err:
            # log db error
            db_logger.error(err)
        finally:
            if con:
                # close DB cursor
                cur.close()
                # close db connection
                con.close()
    # Invalid email or email not in db
    return False

def validate_pass(password1, password2):
    '''Validates user's desired password is not found in list of common passphrases.
    Validates user's desired password against requirements (12 char in length, 1 upper, 1 lower,
    1 special char)
    :return: True if password is valid, else False'''
    error_message = ''
    try:
        with open(COMMON_PASS_PATH, encoding='UTF-8') as f:
            contents = f.read()
            if password1 in contents:
                # if password found in list of common passwords
                error_message = 'Error: Found in list of common passwords. Please try again.'
                # Output error message
                tk.messagebox.showerror(title=None, message=error_message)
                return False
            if len(password1) < 12:
                # if password length is not 12 char
                error_message = 'Invalid length: Password must be greater than 12 characters.'
                # Output error message
                tk.messagebox.showerror(title=None, message=error_message)
                return False
            if not any(char.isdigit() for char in password1):
                # if password does not contain at least one numerical char
                error_message = 'Error: Password must contain at least one numerical character.'
                # Output error message
                tk.messagebox.showerror(title=None, message=error_message)
                return False
            if not any(char.islower() for char in password1):
                # if password does not contain at least one lowercase char
                error_message = 'Error: Password must contain at least one lowercase character.'
                # Output error message
                tk.messagebox.showerror(title=None, message=error_message)
                return False
            if not any(char.isupper() for char in password1):
                # if password does not contain at least one uppercase char
                error_message = 'Error: Password must contain at least one uppercase character.'
                # Output error message
                tk.messagebox.showerror(title=None, message=error_message)
                return False
            if not any(char in SPECIAL_CHAR for char in password1):
                # if password does not contain at least one special char
                error_message = 'Error: Password must contain at least one special character.'
                # Output error message
                tk.messagebox.showerror(title=None, message=error_message)
                return False
            if password1 != password2:
                # if desired password does not match confirmation field
                error_message = 'Error: Passwords do not match.'
                # Output error message
                tk.messagebox.showerror(title=None, message=error_message)
                return False
    except IOError:
        # file not found error
        db_logger.ERROR('Could not find file CommonPassword.txt')
    return True

def check_all_inputs(uname, fname, lname, email, pass1, pass2):
    '''Method to check for validation for all registration input
    :return: tuple(error_message, register)'''
    f_uname = uname.strip().lower()
    f_fname = fname.strip().lower()
    f_lname = lname.strip().lower()
    f_email = email.strip().lower()

    error_message = ''

    while True:
        if check_username_exists(f_uname):
            # if username already exists in db
            error_message = 'Username unavailable'
            # Output error message
            tk.messagebox.showerror(title=None, message=error_message)
            break
        if not validate_username(f_uname):
            error_message = 'Invalid username'
            # Output error message
            tk.messagebox.showerror(title=None, message=error_message)
            break
        if not validate_name(f_fname):
            error_message = 'Invalid first name'
            # Output error message
            tk.messagebox.showerror(title=None, message=error_message)
            break
        if not validate_name(f_lname):
            error_message = 'Invalid last name'
            # Output error message
            tk.messagebox.showerror(title=None, message=error_message)
            break
        if check_email_exists(f_email):
            # if email exists in db (must be unique)
            error_message = 'Invalid Email Address'
            # Output error message
            tk.messagebox.showerror(title=None, message=error_message)
            break
        if not validate_email(f_email):
            #if email is not valid
            error_message = 'Error: Invalid Email Address. \nExample: example@mail.com'
            # Output error message
            tk.messagebox.showerror(title=None, message=error_message)
            print('line 266 dbhelper')
            break
        if validate_pass(pass1, pass2):
            #Inputs are valid and passwords match
            return True
        else:
            break
    # 2Dec Nieves, Chelsea, Valerie
    # Invalid input
    return False

def sign_up(uname, fname, lname, email, pass1, pass2):
    '''Append new user information into table if all inputs are valid
    :return: True if sign up successful, else False'''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()

    #format user input
    f_uname = uname.strip().lower()
    f_fname = fname.strip().lower()
    f_lname = lname.strip().lower()
    f_email = email.strip().lower()

    if check_all_inputs(f_uname, f_fname, f_lname, f_email, pass1, pass2):
        # hash_password = password
        password_byte = pass1.encode('utf-8')
        # generating the salt
        salt = bcrypt.gensalt()
        # Hashing the password
        hash_password = bcrypt.hashpw(password_byte, salt)

        try:
            cur.execute('INSERT INTO user (userId, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)',
                        (uname, fname, lname, email, hash_password))
            con.commit()  # Commit the transaction
            # update registered var to reflect user is registered in DB
            user_logger.info('New registration: %(uname)s')
            return True
        except sqlite3.Error as err:
            # log db error
            db_logger.error(err)
        finally:
            if con:
                cur.close()
                con.close()
                print('The SQLite connection is closed')

    read_sqlite_table()
    # return false if db query or user input invalid
    return False

def auth_user(uname, password):
    '''Authenticates user
    :return: True if user is logged in, else False'''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()

    # call method to validate input and check if uname in db
    if check_username_exists(uname):
        try:
            # query db for password assoc. with uname
            user_password_db = cur.execute('SELECT password FROM user WHERE userID = (?)', (uname,))
            password_db_fetch = user_password_db.fetchone()
            # commit changes to DB
            con.commit()
            # encode db output
            input_password_bytes = password.encode('utf-8')
            # compare passwords
            is_match_password = bcrypt.checkpw(input_password_bytes, password_db_fetch[0])

            if not is_match_password:
                #log error
                user_logger.error('Failed authentication, username: %(uname)s')
            else:
                global username
                global is_user_logged_in
                username = uname
                is_user_logged_in = True
                # log error
                user_logger.info('Successful authentication, username: %(uname)s')
                return True
        except sqlite3.Error as err:
            db_logger.error(err)
        finally:
            if con:
                # close DB cursor
                cur.close()
                con.close()
    else:
        #log error
        user_logger.error('Failed authentication, username %(uname)s does not exist')
    return False

#Valerie Rudich 12/5/2023
#Chelsea Nieves 12/8/23
def sign_out():
    '''Signs user out and resets global variables'''
    global is_user_logged_in
    global username

    if is_user_logged_in and username:
        user_logger.info('User %{username}s signed out successfully')
        is_user_logged_in = False
        username = ''
        return True
    else:
        #message = f''
        user_logger.error('User %{username}s Could Not Be Signed Out!')
        return False

def get_previous_fortunes(uname):
    '''Displays previous fortunes to authenticated user'''
    # if user is authenticated
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()

    previous_fortunes = []
    try:
        # query db for fortunes associated with fk userId
        fortunes_cur = cur.execute('SELECT save_date, category, message FROM fortune WHERE userId = (?)',
                                (uname,))
        res = fortunes_cur.fetchall()
        # commit db session
        con.commit()

        if len(res) > 0: # if user has prev fortunes in db
            header1 = '****DATE  :  CATEGORY  :  FORTUNE****'
            header2 = '------------------------------------------'
            previous_fortunes.append(header1)
            previous_fortunes.append(header2)
            print(header1)
            print(header2)
            for save_date, category, message in res:
                res_strng = f'{save_date}  :  {category}  :  {message}'
                print(res_strng)
                previous_fortunes.append(res_strng)
        else:
            print('No fortunes')
    except sqlite3.Error as err:
        db_logger.error(err)
    finally:
        if con:
            # close DB cursor
            cur.close()
            con.close()
    return previous_fortunes

def save_fortune_to_table(category, fortune):
    ''' Save fortune to authenticated user '''
    global is_user_logged_in
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()

    #get date for save_date column in fortunes
    today = date.today()
    #format date month day, year
    formatted_date = today.strftime('%b %d, %Y')

    if is_user_logged_in:
        try:
            global username
            cur.execute('INSERT INTO fortune (userId, save_date, message, category) VALUES (?, ?, ?, ?)',
                        (username, formatted_date, fortune, category))
            con.commit()  # Commit the transaction
            read_sqlite_table()
            return True
        except sqlite3.Error as err:
            db_logger.error(err)
        finally:
            if con:
                # close DB cursor
                cur.close()
                con.close()
    else:
        tk.messagebox.showerror(title=None, message='Error! Please register or log in to save a fortune.')
        db_logger.error('The user should not be able to access this')
    return False
