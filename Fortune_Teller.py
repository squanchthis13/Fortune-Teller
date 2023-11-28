"""Team 3: Fortune Teller Application
Created By: Constance Sturm, Michelle Cook, Chelsea Nieves,
Valerie Rudich, and Hoi Lam Wong
University of Maryland Global Campus
CMSC 495-7382: Capstone in Computer Science
Professor David Castillo
November 26, 2023"""

import random
import fileinput
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import tkinter as tk


user_fortune = ""

def main():
    """Display Main Menu and Welcome Message"""
    # create root window
    root = Tk()
    # root window and title dimensions
    root.title('Fortune Teller')
    # geometry of the box (width x height)
    root.geometry('350x200')

    # add menu bar to allow user to view rules or exit
    menubar = Menu(root)
    # add Rules menu and commands
    rules = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Rules', menu=rules)
    rules.add_command(label='View Rules', command=lambda: display_rules())
    # add Exit menu and commands
    # updated variable name for menu exit
    program_exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=program_exit)
    program_exit.add_command(label='Exit Program', command=root.destroy)

    # add label to the root window
    lbl1 = Label(root, text='Welcome to the Fortune Teller Game!')
    lbl2 = Label(root, text='Reveal what your future holds!')
    # ask user if they want to play as a guest
    lbl3 = Label(root, text='Would you like to login?')
    lbl1.pack()
    lbl2.pack()
    lbl3.pack()

    # add buttons for user to select yes or no
    btn_login_yes = tk.Button(root, text='Yes', bd='5', command=lambda: login())
    btn_login_no = tk.Button(root, text='No', bd='5', command=lambda: guest_menu())

    btn_login_yes.pack()
    btn_login_no.pack()
    # display menu
    root.config(menu=menubar)
    root.mainloop()


def login():
    """This function is used for returning users"""


# Added new registration form
def guest_menu():
    # Create a guest menu window
    guest = Tk()
    guest.geometry('300x200')
    guest.title('Guest Form')
    lbl_guest = Label(guest, text='Would you like to play as a guest?')
    lbl_guest.pack()
    # add buttons for the user to select their answer
    btn_fortune_menu = tk.Button(guest, text='Yes', bd='5', command=lambda: fortune_menu())
    btn_register = tk.Button(guest, text='No', bd='5', command=lambda: registration())
    btn_fortune_menu.pack()
    btn_register.pack()


def registration():
    # have the user register as a login user
    reg = Tk()
    reg.geometry('300x200')
    reg.title('Registration Form')
    # create new frame to contain the labels and entry boxes
    frm_form = Frame(relief=SUNKEN, borderwidth=3)
    frm_form.pack()

    # COMMENTED OUT 11/27 Hoi
    # It doesn't seem to work on my end, so I have included a new form.

    # # List the field labels
    # labels = [
    #     "First Name"
    #     "Last Name"
    #     "Username"
    #     "Password"
    #     "e-mail"
    # ]
    # # loop for the different labels
    # for idx, text in enumerate(labels):
    #     # create label widget with the text
    #     label = Label(master=frm_form, text=text)
    #     # create an entry widget
    #     entry = Entry(master=frm_form, width=50 )
    #     # grid geometry manager
    #     label.grid(row=idx, column=0, sticky='e')
    #     entry.grid(row=idx, column=1)

    # # create new frame to contain submit and clear button
    # frm_buttons = Frame()
    # frm_buttons.pack(fill=X, ipadx=5, ipady=5)
    # # Submit button
    # btn_submit = Button(master=frm_buttons, text='Submit', command=lambda: database())
    # btn_submit.pack(side=RIGHT, padx=10, ipadx=10)
    # # Clear button
    # btn_clear = Button(master=frm_buttons, text='Clear')
    # btn_clear.pack(side=RIGHT, ipadx=10)

    '''Created 11/27/23 Hoi'''
    # Reference : https://www.tutorialspoint.com/simple-registration-form-using-python-tkinter
    a = Label(reg, text="First Name:")
    a.grid(row=0, column=0)
    b = Label(reg, text="Last Name:")
    b.grid(row=1, column=0)
    c = Label(reg, text="Username:")
    c.grid(row=2, column=0)
    d = Label(reg, text="Password:")
    d.grid(row=3, column=0)
    a1 = Entry(reg)
    a1.grid(row=0, column=1)
    b1 = Entry(reg)
    b1.grid(row=1, column=1)
    c1 = Entry(reg)
    c1.grid(row=2, column=1)
    d1 = Entry(reg)
    d1.grid(row=3, column=1)

    btn_submit = Button(master=reg, text="Submit", command=lambda: handle_registration_submit())
    btn_submit.grid(row=4, column=0)

    # Receive user input and submit form
    # Needs work (connect to database)
    def handle_registration_submit():
        """ This function will be used to save registrations/fortunes"""
        print("submitted!")


# Modified 11/27/23 for formatting.
# Added button to handle potential action
def display_rules():
    """ Create a window that displays the rules to the user"""
    rules = Tk()
    rules.geometry('300x200')
    rules.title('Rules of the Fortune Teller')
    lbl = Label(rules, text='How to Play the Fortune Teller Game', font='50')
    lbl.pack()
    msg = Message(rules, text='> Please select a category from the drop down menu. \n '
                              '> The program will display the fortune to you automatically. \n'
                              '> The program will automatically save your fortune '
                              '> if you are logged in as a returning user. \n'
                              '> Use the menu selection Exit from the '
                              '> main window to exit the program.\n')
    msg.pack()
    btn_rule_close = tk.Button(rules, text='Close Rules', bd='5', command=lambda: rules_option1())
    btn_rule_close.pack()

    def rules_option1():
        """ Method to handle button click to close rules after user has viewed the rules"""
        # Close out rules window
        rules.destroy()


def fortune_menu():
    """This menu will give the user the option to choose a category"""
    fortune = Tk()
    fortune.title('Fortune Menu')

    # Create menu bar
    menubar = Menu(fortune)

    # Add file menu for save and exit options
    file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file)
    file.add_command(label='New Fortune', command=lambda: fortune_menu())
    file.add_command(label='Save', command=lambda: database())
    file.add_separator()
    file.add_command(label='Exit', command=fortune.destroy)

    lbl = Label(fortune, text='Please select a category!')
    btn_love = Button(fortune, text='Love', command=lambda: love_fortune())
    btn_career = Button(fortune, text='Career', command=lambda: career_fortune())
    btn_health = Button(fortune, text='Health', command=lambda: health_fortune())
    btn_general = Button(fortune, text='General', command=lambda: general_fortune())
    btn_random = Button(fortune, text='Random', command=lambda: random_fortune())

    lbl.pack()
    btn_love.pack()
    btn_career.pack()
    btn_health.pack()
    btn_general.pack()
    btn_random.pack()

def display_fortune():
    """This window will display the user's fortune"""
    fortune = Tk()
    fortune.title('Fortune')

    # Create menu bar
    menubar = Menu(fortune)

    # Add file menu for save and exit options
    file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file)
    file.add_command(label='New Fortune', command=lambda: fortune_menu())
    file.add_command(label='Save', command=lambda: database())
    file.add_separator()
    file.add_command(label='Exit', command=fortune.destroy)

    lbl = Label(fortune, text='Please select a category!')
    btn_love = Button(fortune, text='Love', command=lambda: love_fortune())
    btn_career = Button(fortune, text='Career', command=lambda: career_fortune())
    btn_health = Button(fortune, text='Health', command=lambda: health_fortune())
    btn_general = Button(fortune, text='General', command=lambda: general_fortune())
    btn_random = Button(fortune, text='Random', command=lambda: random_fortune())

    lbl.pack()
    btn_love.pack()
    btn_career.pack()
    btn_health.pack()
    btn_general.pack()
    btn_random.pack()
    print(user_fortune)

def love_fortune():
    fortune = []
    file1 = open('love_fortune.txt', 'r')
    lines = file1.read().splitlines()

    for line in lines:
        fortune.append(line)
    user_fortune = random.choice(fortune)


def career_fortune():
    fortune = []
    file1 = open('career_fortune.txt', 'r')
    lines = file1.read().splitlines()

    for line in lines:
        fortune.append(line)
    print(random.choice(fortune))


def health_fortune():
    fortune = []

    file1 = open('health_fortune.txt', 'r')
    lines = file1.read().splitlines()

    for line in lines:
        fortune.append(line)
    print(random.choice(fortune))


def general_fortune():
    fortune = []

    # Testing health fortune. Txt is split by new line
    file1 = open('general_fortune.txt', 'r')
    lines = file1.read().splitlines()

    for line in lines:
        fortune.append(line)
    print(random.choice(fortune))


def random_fortune():
    fortune = []

    # Open multiple text files
    with open('love_fortune.txt', 'r') as file_love, open('general_fortune.txt', 'r') as file_general, open('health_fortune.txt', 'r') as file_health:
        # Read text files and split by line
        lines_love = file_love.read().splitlines()
        lines_general = file_general.read().splitlines()
        lines_health = file_health.read().splitlines()

        # Append lines to fortune
        for line in lines_love:
            fortune.append(line)
        for line in lines_general:
            fortune.append(line)
        for line in lines_health:
            fortune.append(line)
        print(random.choice(fortune))


def database():
    """ This function will be used to save registrations/fortunes"""
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
