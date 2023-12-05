'''Team 3: Fortune Teller Application
Created By: Constance Sturm, Michelle Cook, Chelsea Nieves,
Valerie Rudich, and Hoi Lam Wong
University of Maryland Global Campus
CMSC 495-7382: Capstone in Computer Science
Professor David Castillo
November 26, 2023'''

##NEW NEW NEW
#Pylint
#Wildcard import tkinter (wildcard-import)
from tkinter import *
#NEW NEW NEW
#Pylint
#Wildcard import tkinter.ttk (wildcard-import)
from tkinter.ttk import *
import tkinter as tk

import databasehelper as DBHelper
#NEW NEW NEW 
#Pylint
#FortuneTeller/Fortune-Teller-2/fortune_teller.py:14:0: W0614: 
# Unused import(s) random, LOVE_FORTUNE_PATH, CAREER_FORTUNE_PATH, GENERAL_FORTUNE_PATH, HEALTH_FORTUNE_PATH and db_logger from wildcard import of fthelper 
# (unused-wildcard-import)
from fthelper import *

# create root window
root = Tk()

# Constance Sturm 11/26/2023, 12/5/23
def display_rules():
    ''' Create a window that displays the rules to the user'''

    # Initialize New Window
    rules_tk = Tk()
    rules_tk.geometry('350x260')
    rules_tk.title('Rules of the Fortune Teller')
    center_window(rules_tk)

    # add menu bar to allow user to view rules, fortune,or exit
    menubar = Menu(rules_tk)

    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())

    # add fortune menu and commands
    frtne_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Fortune', menu=frtne_menu)
    frtne_menu.add_command(label='View Fortune', command=lambda: fortune_menu())

    # add Exit menu and commands
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)
    
    lbl = Label(rules_tk, text='How to Play the Fortune Teller Game', font='50')
    lbl.pack()
    msg = Message(rules_tk, text='> Please select a category from the following buttons. \n '
                                 '> The program will display the fortune to you automatically. \n'
                                 '> The program will save your fortune '
                                 '> if you are logged in as a returning user and select save from menu. \n'
                                 '> Use the menu selection Exit to exit the program.\n')
    msg.pack()
    btn_rule_close = tk.Button(rules_tk, text='Close', bd='5', command=rules_tk.destroy)
    btn_rule_close.pack()

# Constance Sturm 11/26/2023, 12/5/23 
def login_window():
    '''This function is used for returning users'''

    # Initialize New Window
    login_tk = Tk()
    login_tk.geometry('300x100')
    login_tk.title('User Login')
    center_window(login_tk)

    # add menu bar to allow user to view rules, fortune,or exit
    menubar = Menu(login_tk)

    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())

    # add fortune menu and commands
    frtne_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Fortune', menu=frtne_menu)
    frtne_menu.add_command(label='View Fortune', command=lambda: fortune_menu())

    # add Exit menu and commands
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)
    
    # create new frame to contain the labels and entry boxes
    login_form = Frame(relief=SUNKEN, borderwidth=3)
    login_form.pack()

    username_login_label = Label(login_tk, text='Username:')
    username_login_label.grid(row=0, column=0)
    password_login_label = Label(login_tk, text='Password:')
    password_login_label.grid(row=1, column=0)

    username_login_entry = Entry(login_tk)
    username_login_entry.grid(row=0, column=1)

    password_login_entry = Entry(login_tk, show='*')

    password_login_entry.grid(row=1, column=1)

    btn_login_submit = Button(master=login_tk, text='Login', command=lambda: user_login())
    btn_login_submit.grid(row=2, column=0)
    btn_login_close = Button(login_tk, text='Cancel', command=login_tk.destroy)
    btn_login_close.grid(row=2, column=1)

    # Hoi Lam Wong 12/4/2023
    def user_login():
        uname = username_login_entry.get().lower().strip()
        password = password_login_entry.get().strip()

        error_message, logged_in = DBHelper.auth_user(uname, password)
        if logged_in == 'True':
            login_tk.destroy()
            # hide root window when user logged in
            global root
            root.withdraw()
            user_menu()
        else:
            login_message_window(error_message)

    login_tk.mainloop()


# Hoi Lam Wong 11/27/2023
def login_message_window(error_message):
    ''' New window that show whether sign up is successful or not'''

    login_result_tk = Tk()
    login_result_tk.geometry('400x150')
    login_result_tk.title('User Register')
    center_window(login_result_tk)

    # Dynamically set message to show sign up confirmation
    message = ''
    if error_message == '':
        # There is no error if error message is empty
        message = 'Log In Successful!'
    else:
        # Else message to be displayed is the error message
        message = error_message

    # Create label for message
    login_result_label = Label(login_result_tk, text=message)
    login_result_label.pack()

    # Create button for closing window
    btn_close = Button(login_result_tk, text='Close', command=login_result_tk.destroy)
    btn_close.pack()

    login_result_tk.mainloop()


# Hoi Lam Wong 11/27/2023
# Constance Sturm 12/5/23 added menu bar for uniformity
def registration_window():
    ''' This function is used to create new window that holds registration from '''

    # Initialize New Window
    registration_tk = Tk()
    registration_tk.geometry('350x350')
    registration_tk.title('Registration Form')
    center_window(registration_tk)

    # add menu bar to allow user to view rules, fortune,or exit
    menubar = Menu(registration_tk)

    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())

    # add fortune menu and commands
    fortune_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Fortune', menu=fortune_menu)
    fortune_menu.add_command(label='View Fortune', command=lambda: fortune_menu())

    # add Exit menu and commands
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)
    
    # create new frame to contain the labels and entry boxes
    frm_form = Frame(relief=SUNKEN, borderwidth=3)
    frm_form.pack()

    first_name_label = Label(registration_tk, text='First Name:')
    first_name_label.grid(row=0, column=0)
    last_name_label = Label(registration_tk, text='Last Name:')
    last_name_label.grid(row=1, column=0)
    username_label = Label(registration_tk, text='Username:')
    username_label.grid(row=2, column=0)
    email_label = Label(registration_tk, text='Email:')
    email_label.grid(row=3, column=0)
    password_label = Label(registration_tk, text='Password:')
    password_label.grid(row=4, column=0)
    password_confirm_label = Label(registration_tk, text='Confirm Password:')
    password_confirm_label.grid(row=5, column=0)

    first_name_entry = Entry(registration_tk)
    first_name_entry.grid(row=0, column=1)
    last_name_entry = Entry(registration_tk)
    last_name_entry.grid(row=1, column=1)
    username_entry = Entry(registration_tk)
    username_entry.grid(row=2, column=1)
    email_entry = Entry(registration_tk)
    email_entry.grid(row=3, column=1)
    password_entry = Entry(registration_tk, show='*')
    # password_entry = Entry(registration_tk)
    password_entry.grid(row=4, column=1)
    password_confirm_entry = Entry(registration_tk, show='*')
    password_confirm_entry.grid(row=5, column=1)

    btn_submit = Button(master=registration_tk, text='Submit',
                        command=lambda: user_register())
    btn_submit.grid(row=6, column=0)
    btn_close = Button(registration_tk, text='Close', command=registration_tk.destroy)
    btn_close.grid(row=6, column=1)

    def user_register():
        '''Method for registration() for backend
        Note: This method is part of/inside of method registration()
        '''
        # Get value from text boxes
        uname = username_entry.get()
        fname = first_name_entry.get()
        lname = last_name_entry.get()
        email = email_entry.get()
        pass1 = password_entry.get()
        pass2 = password_confirm_entry.get()

        # 2Dec Nieves, Chelsea
        # Assign returned tuple
        error_message, registered = DBHelper.sign_up(uname, fname, lname, email, pass1, pass2)
        if registered == 'True':
            # destroy registration form if successfully signed up
            registration_tk.destroy()

        # Call method to create new window that contains the confirmation/ error message
        registration_message_window(error_message)

    # Call to create registration_tk... END of registration TK
    registration_tk.mainloop()


# Hoi Lam Wong 11/27/2023
def registration_message_window(error_message):
    ''' New window that show whether sign up is successful or not'''

    submission_result_tk = Tk()
    submission_result_tk.geometry('400x100')
    submission_result_tk.title('User Register')
    center_window(submission_result_tk)

    # Dynamically set message to show sign up confirmation
    message = ''
    if error_message == '':
        # There is no error if error message is empty
        message = 'Registration Successful! Please Log In'
    else:
        # Else message to be displayed is the error message
        message = error_message

    # Create label for message
    submission_result_label = Label(submission_result_tk, text=message)
    submission_result_label.pack()

    # Create button for closing window
    btn_close = Button(submission_result_tk, text='Close', command=submission_result_tk.destroy)
    btn_close.pack()

    submission_result_tk.mainloop()


# Constance 11/27/2023, 12/5/23 
def fortune_menu():
    '''This menu will give the user the option to choose a category'''

    # Initialize New Window
    fortune_menu_tk = Tk()
    fortune_menu_tk.geometry('300x200')
    fortune_menu_tk.title('Fortune Menu')
    center_window(fortune_menu_tk)

    # Valerie Rudich 12/5/2023
    # Constance Sturm added additions to the menubar to keep it uniform 
    # add menu bar to allow user to view rules, fortune,or exit
    menubar = Menu(fortune_menu_tk)

    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())

    # add fortune menu and commands
    frtne_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Fortune', menu=frtne_menu)
    frtne_menu.add_command(label='View Fortune', command=lambda: fortune_menu())

    # add Exit menu and commands
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)
    
    lbl = Label(fortune_menu_tk, text='Please select a category!')
    btn_love = Button(fortune_menu_tk, text='Love', command=lambda: display_fortune('Love'))
    btn_career = Button(fortune_menu_tk, text='Career', command=lambda: display_fortune('Career'))
    btn_health = Button(fortune_menu_tk, text='Health', command=lambda: display_fortune('Health'))
    btn_general = Button(fortune_menu_tk, text='General', command=lambda: display_fortune('General'))
    btn_random = Button(fortune_menu_tk, text='Random', command=lambda: display_fortune('Random'))

    lbl.pack()
    btn_love.pack()
    btn_career.pack()
    btn_health.pack()
    btn_general.pack()
    btn_random.pack()

    fortune_menu_tk.mainloop()

# Hoi Lam Wong 11/28/2023
# Constance Sturm 12/5/23 added menubar for uniformity 
def display_fortune(category):
    ''' Method to create a new window to display user's fortune 
    based on the category they choose in fortune menu'''

    user_fortune = ''
    if category == 'Love':
        user_fortune = get_love_fortune()
    elif category == 'Career':
        user_fortune = get_career_fortune()
    elif category == 'General':
        user_fortune = get_general_fortune()
    elif category == 'Health':
        user_fortune = get_health_fortune()
    elif category == 'Random':
        user_fortune = get_random_fortune()

    # Initialize New Window
    fortune_tk = Tk()
    fortune_tk.title('Fortune Menu')
    fortune_tk.geometry('300x200')
    center_window(fortune_tk)

    # add menu bar to allow user to view rules, fortune,or exit
    menubar = Menu(fortune_tk)

    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())

    # add fortune menu and commands
    frtne_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Fortune', menu=frtne_menu)
    frtne_menu.add_command(label='View Fortune', command=lambda: fortune_menu())

    # add Exit menu and commands
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)
    
    lbl = Label(fortune_tk, text='Your Fortune', font='50')
    lbl.pack()
    lbl_category = Label(fortune_tk, text=category, font='40')
    lbl_category.pack()

    fortune_message = Message(fortune_tk, text=user_fortune)
    fortune_message.pack()

    btn_fortune_new = tk.Button(fortune_tk, text='New Fortune', bd='2', command=fortune_tk.destroy)
    btn_fortune_new.pack()
    # Valerie Rudich 12/5/2023
    # adds save option only if the user is signed in

    #NEW NEW NEW
    #Pylint
    #FortuneTeller/Fortune-Teller-2/fortune_teller.py:299:7: C0121: Comparison 'DBHelper.is_user_logged_in == True' should be 'DBHelper.is_user_logged_in is True' 
    #if checking for the singleton value True, or 'DBHelper.is_user_logged_in' if testing for truthiness (singleton-comparison)
    if DBHelper.is_user_logged_in == True:
        btn_fortune_save = tk.Button(fortune_tk, text='Save', bd='2', command=lambda: [save_fortune_confirm_window(fortune_tk)])
        btn_fortune_save.pack()

    # Hoi Lam Wong 12/4/2023
    def save_fortune_confirm_window(win):
        '''
        Method to create a new window that confirms whether a fortune is saved to the database
        '''
        win.destroy()
        save_fortune_confirm_tk = Tk()
        save_fortune_confirm_tk.geometry('400x150')
        save_fortune_confirm_tk.title('User Register')
        center_window(save_fortune_confirm_tk)

        save_fortune_confirm_message = DBHelper.save_fortune_to_table(category, user_fortune)
        # Create label for message
        save_fortune_result_label = Label(save_fortune_confirm_tk, text=save_fortune_confirm_message)
        save_fortune_result_label.pack()

        # Create button for closing window
        btn_close = Button(save_fortune_confirm_tk, text='Close', command=save_fortune_confirm_tk.destroy)
        btn_close.pack()

        save_fortune_confirm_tk.mainloop()

    fortune_tk.mainloop()


# Hoi Lam Wong 12/4/2023
# Constance Sturm 12/5/23 added menubar for uniformity
def past_fortunes_window():
    ''' Method to create new window for displaying user's past fortunes '''
    # Check if user is logged in
    if DBHelper.is_user_logged_in:
        username = DBHelper.username
    else:
        username = 'GUEST: Not Logged In'

    def create_past_fortunes_table(win):

        past_fortunes = DBHelper.get_previous_fortunes(username)

        ''' method to create table in win with dynamic height (rows) from data '''
        # Create table frame widget
        past_fortunes_table_frame = tk.Frame(win)
        past_fortunes_table_frame.grid(row=1, column=0, padx=10, pady=10)

        scrollbar = Scrollbar(past_fortunes_table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        mylist = Listbox(past_fortunes_table_frame, yscrollcommand=scrollbar.set, width=75)
        for row in past_fortunes:
            mylist.insert(END, row)

        mylist.pack(side=LEFT, fill=BOTH)

        scrollbar.config(command=mylist.yview)

    # Initialize New Window
    previous_fortunes_tk = Tk()
    previous_fortunes_tk.title('Past Fortunes')
    previous_fortunes_tk.geometry('510x300')
    center_window(previous_fortunes_tk)

    # add menu bar to allow user to view rules, fortune,or exit
    menubar = Menu(previous_fortunes_tk)

    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())

    # add fortune menu and commands
    frtne_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Fortune', menu=frtne_menu)
    frtne_menu.add_command(label='View Fortune', command=lambda: fortune_menu())

    # add Exit menu and commands
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)
    
    # Username label
    username_label = Label(previous_fortunes_tk, text=username)
    username_label.grid(row=0, column=0)

    # Create table
    create_past_fortunes_table(previous_fortunes_tk)

    # Button for Action
    btn_close = tk.Button(previous_fortunes_tk, text='Close', bd='5', command=previous_fortunes_tk.destroy)
    btn_close.grid(row=2, column=0)

    previous_fortunes_tk.mainloop()

# Valerie Rudich 12/4/2023
# Constance Sturm 12/5/23 updated menubar to create uniformity
def user_menu():
    '''New menu once user is logged in to choose new fortune or view old fortunes'''

    # Initialize New Window
    user_menu_tk = Tk()
    user_menu_tk.geometry('650x400')
    user_menu_tk.title('Fortune Teller')
    center_window(user_menu_tk)

    # add menu bar to allow user to view rules, fortune,or exit
    menubar = Menu(user_menu_tk)

    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())

    # add fortune menu and commands
    frtne_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Fortune', menu=frtne_menu)
    frtne_menu.add_command(label='View Fortune', command=lambda: fortune_menu())

    # add Exit menu and commands
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)
    
    # add Sign Out menu and commands
    #NEW
    sign_out = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Sign Out', menu=sign_out)
    sign_out.add_command(label='Sign Out', command=lambda: signout_window(user_menu_tk))

    # add label and buttons to the window
    welcome_user_message = 'Welcome Back, ' + DBHelper.username + ' to the Fortune Teller Game!'
    lbl1 = Label(user_menu_tk, text=welcome_user_message)
    lbl2 = Label(user_menu_tk, text='Reveal what your future holds!')
    lbl1.pack()
    lbl2.pack()

    # add crystal ball ascii art
    crystal_ball_ascii_art(user_menu_tk)

    btn_get_frtn = Button(user_menu_tk, text='Get a Fortune', command=lambda: fortune_menu())
    btn_past_frtn = Button(user_menu_tk, text='View Past Fortune', command=lambda: past_fortunes_window())

    btn_get_frtn.pack()
    btn_past_frtn.pack()
    user_menu_tk.config(menu=menubar)

    user_menu_tk.mainloop()

# Valerie Rudich 12/5/2023
# Constance Sturm 12/5/23 added menubar to keep uniformity
def signout_window(user_menu_tk):
    '''This function is used for signing users out and returning to main menu'''

    # Initialize New Window
    signout_tk = Tk()
    signout_tk.geometry('300x125')
    signout_tk.title('Sign Out')
    center_window(signout_tk)

    # add menu bar to allow user to view rules, fortune,or exit
    menubar = Menu(signout_tk)

    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())

    # add fortune menu and commands
    frtne_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Fortune', menu=frtne_menu)
    frtne_menu.add_command(label='View Fortune', command=lambda: fortune_menu())

    # add Exit menu and commands
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)
    
    # add label and buttons to window
    sign_out_message = 'Confirm ' + DBHelper.username + ' Sign Out'
    lbl1 = Label(signout_tk, text=sign_out_message)

    lbl1.pack()

    btn_yes = Button(signout_tk, text='Yes', command=lambda: user_sign_out())
    btn_no = Button(signout_tk, text='No', command=signout_tk.destroy)

    btn_yes.pack()
    btn_no.pack() 

    # Valerie Rudich 12/5/2023
    #NEW
    def user_sign_out():
        signout_message = DBHelper.sign_out()
        lbl2 = Label(signout_tk, text=signout_message)
        lbl2.pack()
        signout_tk.after(2000, signout_tk.destroy)
        user_menu_tk.destroy()
        # Hoi 12/5/23 Modify to un-hide root
        global root
        root.deiconify()

    signout_tk.mainloop()

# Constance Sturm 11/27/2023, 12/5/23 updated menubar for uniformity
# Heavily Modified by Hoi Lam Wong 12/2/2023
def main_window():
    '''Display Main Menu and Welcome Message'''
    
    #NEW NEW NEW
    #Pylint
    #FortuneTeller/Fortune-Teller-2/fortune_teller.py:462:8: C0121: Comparison 'DBHelper.active == False' 
    #should be 'DBHelper.active is False' if checking for the singleton value False, or 'not DBHelper.active' if testing for falsiness (singleton-comparison)
    if (DBHelper.active == False):
        DBHelper.create_table()
        print('Table created')
        # test_create_table()

    # root window and title dimensions
    root.title('Fortune Teller')
    # geometry of the box (width x height)
    root.geometry('650x415')
    # center window
    center_window(root)

    # add menu bar to allow user to view rules, fortune,or exit
    menubar = Menu(root)

    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())

    # add fortune menu and commands
    frtne_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Fortune', menu=frtne_menu)
    frtne_menu.add_command(label='View Fortune', command=lambda: fortune_menu())

    # add Exit menu and commands
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)
    
    # add label to the root window
    lbl1 = Label(root, text='Welcome to the Fortune Teller Game!')
    lbl2 = Label(root, text='Reveal what your future holds!')
    lbl1.pack()
    lbl2.pack()

    # add crystal ball ascii art
    crystal_ball_ascii_art(root)

    # Changed Buttons to include more options
    btn_play = tk.Button(root, text='Play as Guest', bd='1', command=lambda: fortune_menu())
    btn_login = tk.Button(root, text='Login', bd='1', command=lambda: login_window())
    btn_register = tk.Button(root, text='Register', bd='1', command=lambda: registration_window())

    btn_play.pack()
    btn_login.pack()
    btn_register.pack()

    # display menu
    root.config(menu=menubar)
    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #test
    main_window()
