from tkinter import *
import random
from LogHandler import db_logger

def center_window(win):
    """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def crystal_ball_ascii_art(win):
    """ Function to add a label with crystal ball ascii art to window win"""

    def pad_to_center(l: list, w: int) -> str:
        """Helper Method for Manual centering ascii art"""
        padding = ' ' * (w // 2)  # a 1 char line would need at most w/2 spaces in front
        parts = [padding[0: (w - len(p)) // 2 + 1] + p for p in l]
        return '\n'.join(parts)

    crystal_ball_raw = r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠾⠛⠋⠉⠉⠉⠉⢙⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢀⣼⠟⠁⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⡟⣷⡀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣾⢇⣤⣶⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠁⢹⣇⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⢠⡿⠁⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⣠⣤⡙⠻⢿⣿⣿⣿⣿⣿⣋⣠⣤⡶⠟⢁⣤⡄⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢿⣿⣿⣷⣤⣈⣉⠉⠛⠛⠉⣉⣠⣤⣾⣿⣿⡟⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⣾⣦⣀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⢋⣠⣴⣷⠀⠀⠀⠀
    ⠀⠀⠀⠀⢿⣿⣿⣿⣷⣶⣤⣬⣭⣉⣉⣉⣩⣭⣥⣤⣶⣾⣿⣿⣿⡿⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠛⠛⠛⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        """

    crystal_ball_text = pad_to_center(crystal_ball_raw.split('\n'), 60)
    Label(win, justify=LEFT, text=crystal_ball_text).pack()

def get_love_fortune():
    try:
        with open('texts/love_fortune.txt', 'r', encoding = 'utf-8') as file:
            all_text: str = file.read()
            fortune = list(map(str, all_text.split(':')))
            # Print random fortune from love_fortune.txt
            return random.choice(fortune)
    except IOError as err:
        print('Unable to find file love_fortune.txt')
        db_logger.error(err)

def get_career_fortune():
    try:
        with open('texts/career_fortune.txt', 'r', encoding = 'utf-8') as file:
            all_text: str = file.read()
            fortune = list(map(str, all_text.split(':')))
            # Print random fortune from career_fortune.txt
            return random.choice(fortune)
    except IOError as err:
        print('Unable to find file career_fortune.txt')
        db_logger.error(err)

def get_health_fortune():
    try:
        with open('texts/health_fortune.txt', 'r', encoding = 'utf-8') as file:
            all_text: str = file.read()
            fortune = list(map(str, all_text.split(':')))
            # Print random fortune from health_fortune.txt
            return random.choice(fortune)
    except IOError as err:
        print('Unable to find file health_fortune.txt')
        db_logger.error(err)

def get_general_fortune():
    try:
        with open('texts/general_fortune.txt', 'r', encoding = 'utf-8') as file:
            all_text: str = file.read()
            fortune = list(map(str, all_text.split(':')))
            # Print random fortune from general_fortune.txt
            return random.choice(fortune)
    except IOError as err:
        print('Unable to find file general_fortune.txt')
        db_logger.error(err)

def get_random_fortune():
    try:
        with fileinput.input(
                files=("love_fortune.txt", "career_fortune.txt", "health_fortune.txt", "general_fortune.txt")) as file:
            all_text: str = file.read()
            fortune = list(map(str, all_text.split(":")))
            # Print random fortune from any of the .txt files
            return random.choice(fortune)
    except IOError as err:
        db_logger.error(err)