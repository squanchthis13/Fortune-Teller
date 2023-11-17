"""Team 3: Fortune Teller Application
Created By: Constance Sturm, Michelle Cook, Chelsea Nieves,
Valerie Rudich, and Hoi Lam Wong
University of Maryland Global Campus
CMSC 495-7382: Capstone in Computer Science
Professor David Castillo
November 17, 2023"""

import sys
import random
import time
import fileinput


def main():
    """Display Main Menu and Welcome Message"""
    print('Welcome to the Fortune Teller Game!')
    print('Reveal what your future holds!')
    # call main menu for user selection
    main_menu()


def main_menu():
    """Display the Main Menu for user selection."""
    print('\nPlease select from the following menu: ')
    print('\n 1. Rules')
    print('\n 2. Choose a Fortune')
    print('\n 0. Exit the Program')
    user_selection = input('Enter Selection Here: ')
    if user_selection == 1:
        display_rules()
    elif user_selection == 2:
        fortune_menu()
    elif user_selection == 0:
        print('Thank you for using the fortune teller game!')
        print('\nGoodbye!')
        sys.exit()
    else:
        print('Error! Invalid Selection!)')
        print('\nPlease enter a number between 0-2!')
        user_selection = input('\nEnter Selection Here: ')


def display_rules():
    print('')
    print('')
    print('')
    time.sleep(120)


def fortune_menu():
    print('Please choose a fortune category from the following menu:')
    print('\n 1. Love')
    print('\n 2. Career')
    print('\n 3. Health')
    print('\n 4. General')
    print('\n 5. Random Fortune')
    user_choice = input('\nEnter Selection Here: ')
    if user_choice == 1:
        love_fortune()
    elif user_choice == 2:
        career_fortune()
    elif user_choice == 3:
        health_fortune()
    elif user_choice == 4:
        general_fortune()
    elif user_choice == 5:
        random_fortune()
    else:
        print('Error! Invalid Selection!')
        print('\nPlease enter a number between 1-5!')
        user_choice = input('\nEnter Selection Here: ')


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
