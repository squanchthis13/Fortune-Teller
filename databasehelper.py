'''
Module to create db, tables, and query/output data
'''
import sqlite3
import string
import re
import bcrypt
from datetime import date
from loghandler import user_logger, db_logger

SPECIAL_CHAR = string.punctuation  # special characters to validate password requirements
DB_NAME = 'FortuneTeller.db' # Create a new database
COMMON_PASS_PATH = 'texts/CommonPassword.txt'
is_user_logged_in = False
username = ''
active = False # var if db has been created

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
    ''' Creates 3 SQL tables to store user and previous fortune data '''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()
    try:
        cur.executescript('''
        CREATE TABLE IF NOT EXISTS user(userId VARCHAR(20) NOT NULL PRIMARY KEY, first_name TEXT(20) NOT NULL, last_name TEXT(20) NOT NULL, email VARCHAR(20) NOT NULL, password BLOB);
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

def check_username_exists(input_username):
    '''Method to check if username already exists in db
    :return: boolean True if exists, else False
    '''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()
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

def check_all_inputs(uname, fname, lname, email, pass1, pass2):
    '''Method to check for validation for all input
    :return: tuple(error_message, register)'''
    uname = uname.lower().strip()
    error_message = ''
    ### NEW NEW NEW ###
    # 2Dec Nieves, Chelsea
    # Added variables to check validity of user input
    valid = 'False'  # var to track if input is valid; default is False
    register = 'False'  # var to track if user is able to register; default is False

    if check_username_exists(uname):
        # call method to query database by username to determine if username is already registered
        error_message = 'Username unavailable'
    ### NEW NEW NEW ###
    # 2Dec Nieves, Chelsea
    # Modified elif to include fname and lname not null/blank
    # Will need to add email field
    elif uname == '' or fname == '' or lname == '':
        # Fields cannot be left blank
        error_message = 'Field cannot be left blank.'
    elif email == '' or pass1 == '' or pass2 == '':
        # Fields cannot be left blank
        error_message = 'Field cannot be left blank.'
    else:
        ### NEW NEW NEW ###
        # 2Dec Nieves, Chelsea, Valerie
        # Assign returned tuple

        error_message, valid = validate_pass(pass1, pass2)
        error_message2, valid2 = validate_email(email)

        # if all input fields valid, valid == 'True'
        if valid == 'True' and valid2 == 'True':
            # if valid == 'True', allow user to register
            register = 'True'
    ### NEW NEW NEW ###
    # 2Dec Nieves, Chelsea, Valerie
    # Invalid input
    # Return success/error message and registration state
    #return error_message, register
    if error_message2 != '':
        return error_message2, register
    return error_message, register

# Valerie Rudich 12/5/2024
#NEW
def validate_email(email):
    '''Validates user's email address
    :return: tuple(error_message, valid)'''
    error_message = 'Error: Invalid Email Address'
    valid = 'False'
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, email):
        error_message = ''
        valid = 'True'

    return error_message, valid

def validate_pass(password1, password2):
    '''Validates user's desired password is not found in list of common passphrases.
    Validates user's desired password against requirements (12 char in length, 1 upper, 1 lower,
    1 special char)
    :return: tuple(error_message, valid)'''
    error_message = ''
    valid = 'False'  # var to track if user is able to register; default is False
    try:
        with open(COMMON_PASS_PATH, encoding='UTF-8') as f:
            contents = f.read()
            if password1 in contents:
                # if password found in list of common passwords
                error_message = 'Error: Found in list of common passwords. Please try again.'
            elif len(password1) < 12:
                # if password length is not 12 char
                error_message = 'Invalid length: Password must be greater than 12 characters.'
            elif not any(char.isdigit() for char in password1):
                # if password does not contain at least one numerical char
                error_message = 'Error: Password must contain at least one numerical character.'
            elif not any(char.islower() for char in password1):
                # if password does not contain at least one lowercase char
                error_message = 'Error: Password must contain at least one lowercase character.'
            elif not any(char.isupper() for char in password1):
                # if password does not contain at least one uppercase char
                error_message = 'Error: Password must contain at least one uppercase character.'
            elif not any(char in SPECIAL_CHAR for char in password1):
                # if password does not contain at least one special char
                error_message = 'Error: Password must contain at least one special character.'
            elif password1 != password2:
                # if desired password does not match confirmation field
                error_message = 'Error: Passwords do not match.'
            else:
                ### NEW NEW NEW ###
                # 2Dec Nieves, Chelsea
                # user input is valid, update var
                valid = 'True'
    except IOError:
        # file not found error
        db_logger.ERROR('Could not find file CommonPassword.txt')
    ### NEW NEW NEW ###
    # 2Dec Nieves, Chelsea
    # Invalid input
    # Return success/error message and registration state
    return error_message, valid

def sign_up(uname, fname, lname, email, pass1, pass2):
    '''Append new user information into table if all inputs are valid
    :return: tuple(error_message, registered)'''
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()

    #format user input
    uname = uname.lower().strip()
    fname = fname.lower().strip()
    lname = lname.lower().strip()
    email = email.strip()

    # hash_password = password
    password_byte = pass1.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash_password = bcrypt.hashpw(password_byte, salt)
    # Assign returned tuple
    error_message, register = check_all_inputs(uname, fname, lname, email, pass1, pass2)
    registered = 'False'  # var to track if user is registered; default is False
    # if user input is valid and user is allowed to register
    if register == 'True':
        try:
            cur.execute('INSERT INTO user (userId, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)',
                        (uname, fname, lname, email, hash_password))
            con.commit()  # Commit the transaction
            # update registered var to reflect user is registered in DB
            registered = 'True'
            user_logger.info('New registration: %(uname)s')
        except sqlite3.Error as err:
            # log db error
            db_logger.error(err)
        finally:
            if con:
                cur.close()
                con.close()
                print('The SQLite connection is closed')

    read_sqlite_table()
    # Return success/error message
    # Return registered status
    return error_message, registered

def auth_user(uname, password):
    '''Authenticates user
    :return: tuple(error_message, logged_in)'''
    error_message = ''
    logged_in = 'False'

    # if username exists in db
    if check_username_exists(uname):
        # create DB connection
        con = sqlite3.connect(DB_NAME)
        # create DB cursor
        cur = con.cursor()
        try:
            user_password_db = cur.execute('SELECT password FROM user WHERE userID = (?)', (uname,))
            password_db_fetch = user_password_db.fetchone()
            input_password_bytes = password.encode('utf-8')
            
            is_match_password = bcrypt.checkpw(input_password_bytes, password_db_fetch[0])

            if is_match_password:
                logged_in = 'True'

                global username
                global is_user_logged_in
                username = uname
                is_user_logged_in = True
            else:
                user_logger.error('Failed authentication, username: %(uname)s')
                error_message = 'ERROR: Authentication failed!'
            # commit changes to DB
            con.commit()
        except sqlite3.Error as err:
            db_logger.error(err)
        finally:
            if con:
                # close DB cursor
                cur.close()
                con.close()
    else:
        error_message = 'ERROR: Authentication failed!'
        user_logger.error('Failed authentication, username %(uname)s does not exist')
    return error_message, logged_in

#Valerie Rudich 12/5/2023
def sign_out():
    '''Signs user out and resets global variables'''
    global is_user_logged_in
    global username

    message = f'User {username} Could Not Be Signed Out'

    if is_user_logged_in and username:
        user_logger.info('User %{username}s has been signed out')
        is_user_logged_in = False
        username = ''
        message = 'Successfully Signed Out'
    return message

def get_previous_fortunes(uname):
    '''Displays previous fortunes to authenticated user'''
    # if user is authenticated
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()

    previous_fortunes = []
    try:
        #modified query to output just category and message to user
        fortunes_cur = cur.execute('SELECT save_date, category, message FROM fortune WHERE userId = (?)',
                                (uname,))
        res = fortunes_cur.fetchall()
        con.commit()

        print('PREVIOUS FORTUNES')
        if len(res) > 0:
            for save_date, category, message in res:
                print(save_date + category + ': ' + message)
                previous_fortunes.append(save_date + ' ' + category + ': ' + message)
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
    save_fortune_to_table_message = 'Error! Please register or log in to save a fortune.'

    global is_user_logged_in
    # If user is not logged in already, return message immediately
    if not is_user_logged_in:
        return save_fortune_to_table_message

    # if user is authenticated
    # create DB connection
    con = sqlite3.connect(DB_NAME)
    # create DB cursor
    cur = con.cursor()

    #get date for save_date column in fortunes
    today = date.today()
    #format date month day, year
    formatted_date = today.strftime('%B %d, %Y')

    try:
        global username
        cur.execute('INSERT INTO fortune (userId, save_date, message, category) VALUES (?, ?, ?, ?)',
                    (username, formatted_date, fortune, category))
        con.commit()  # Commit the transaction
        read_sqlite_table()

        save_fortune_to_table_message = 'Fortune Saved!'
    except sqlite3.Error as err:
        db_logger.error(err)
    finally:
        if con:
            # close DB cursor
            cur.close()
            con.close()
    return save_fortune_to_table_message
