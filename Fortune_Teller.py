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
from tkinter.ttk import *
import tkinter as tk



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
    exit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Exit', menu=exit)
    exit.add_command(label='Exit Program', command=root.destroy)

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

# 11/27/23
# Error: cannot use geometry manager pack inside .!frame which already has slaves managed by grid

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
    # display window
    guest.mainloop()


def registration():
    # have the user register as a login user
    reg = Tk()
    reg.geometry('300x200')
    reg.title('Registration Form')
    # create new frame to contain the labels and entry boxes
    frm_form = Frame(relief=SUNKEN, borderwidth=3)
    frm_form.pack()

    # List the field labels
    labels = [
        "First Name"
        "Last Name"
        "Username"
        "Password"
        "e-mail"
    ]
    # loop for the different labels
    for idx, text in enumerate(labels):
        # create label widget with the text
        label = Label(master=frm_form, text=text)
        # create an entry widget
        entry = Entry(master=frm_form, width=50)
        # grid geometry manager
        label.grid(row=idx, column=0, sticky='e')
        entry.grid(row=idx, column=1)
        # pack label to scene
        label.pack()

    # create new frame to contain submit and clear button
    frm_buttons = Frame()
    frm_buttons.pack(fill=X, ipadx=5, ipady=5)
    # Submit button
    btn_submit = Button(master=frm_buttons, text='Submit', command=lambda: database())
    btn_submit.pack(side=RIGHT, padx=10, ipadx=10)
    # Clear button
    btn_clear = Button(master=frm_buttons, text='Clear')
    btn_clear.pack(side=RIGHT, ipadx=10)


def database():
    """ This function will be used to save registrations/fortunes"""


def display_rules():
    """ Create a window that displays the rules to the user"""
    rules = Tk()
    rules.geometry('300x200l')
    rules.title('Rules of the Fortune Teller')
    lbl = Label(rules, text='How to Play the Fortune Teller Game', font='50')
    lbl.pack()
    msg = Message(rules, text='Please select a category from the drop down menu. The program will display the fortune '
                              'to you automatically. The program will automatically save your fortune if you are '
                              'logged in as a returning user. Use the menu selection Exit from the main window to '
                              'exit the program.')
    msg.pack()
    rules.mainloop()


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


def love_fortune():
    with open("love_fortune.txt", "r") as file:
        all_text: str = file.read()
        fortune = list(map(str, all_text.split(":")))
        # Print random fortune from love_fortune.txt
        print(random.choice(fortune))


def career_fortune():
    with open("career_fortune.txt", "r") as file:
        all_text: str = file.read()
        fortune = list(map(str, all_text.split(":")))
        # Print random fortune from career_fortune.txt
        print(random.choice(fortune))


def health_fortune():
    with open("health_fortune.txt", "r") as file:
        all_text: str = file.read()
        fortune = list(map(str, all_text.split(":")))
        # Print random fortune from health_fortune.txt
        print(random.choice(fortune))


def general_fortune():
    with open("general_fortune.txt", "r") as file:
        all_text: str = file.read()
        fortune = list(map(str, all_text.split(":")))
        # Print random fortune from general_fortune.txt
        print(random.choice(fortune))


def random_fortune():
    with fileinput.input(
            files=("love_fortune.txt", "career_fortune.txt", "health_fortune.txt", "general_fortune.txt")) as file:
        all_text: str = file.read()
        fortune = list(map(str, all_text.split(":")))
        # Print random fortune from any of the .txt files
        print(random.choice(fortune))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()