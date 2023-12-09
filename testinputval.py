'''PyUnit tests to test input validation methods
modified: 9Dec23
author: Nieves, Chelsea'''

import unittest
from databasehelper import *

class TestInputVal(unittest.TestCase):
    def test_validate_name(self):
        '''Test valid and invalid inputs to first name and last name fields'''
        #test invalid
        #test blank
        self.assertFalse(validate_name(''))
        #test special char
        self.assertFalse(validate_name('te$t'))
        #test number
        self.assertFalse(validate_name('t3st'))
        #test len > 20 char
        self.assertFalse(validate_name('TestInputisTooLongTest'))
        
        #test valid
        self.assertTrue(validate_name('test'))
    
    #@unittest.skip
    def test_validate_email(self):
        '''Test valid and invalid inputs to email field'''
        #test invalid
        #test blank
        self.assertFalse(validate_email(''))
        #test doesnt match expected pattern
        self.assertFalse(validate_email('test@test'))
        self.assertFalse(validate_email('test.com'))

        #test valid
        self.assertTrue(validate_email('test@test.com'))

    def test_validate_username(self):
        '''Test valid and invalid inputs to username field'''
        #test invalid
        #blank input
        self.assertFalse(validate_username(''))
        #special char
        self.assertFalse(validate_username('te$t'))
        # len > 20
        self.assertFalse(validate_username('TestInputisTooLongTest'))

        #test valid
        #username string + digit
        self.assertTrue(validate_username('test1'))
        #username string
        self.assertTrue(validate_username('test'))

    def test_validate_pass(self):
        '''Test if pass1 and pass2 are valid for user registration'''
        valid_pass = '1qaz!QAZ2wsx@WSX'
        #invalid input
        #blank input
        self.assertFalse(validate_pass('', ''))
        #password in contents; #len < 12; 
        self.assertFalse(validate_pass('test', 'test'))
        #no number
        self.assertFalse(validate_pass('QAZ!qazwsx@WSX', 'QAZ!qazwsx@WSX'))
        #no lower char
        self.assertFalse(validate_pass('1QAZ!QAZ2WSX@WSX', '1QAZ!QAZ2WSX@WSX'))
        #no upper char
        self.assertFalse(validate_pass('1qaz!qaz2wsx@wsx', '1qaz!qaz2wsx@wsx'))
        # no special char
        self.assertFalse(validate_pass('1qazqaz2wsxwsx', '1qazqaz2wsxwsx'))
        # passwords do not match
        self.assertFalse(validate_pass(valid_pass, '@WSXxsw2!QAZzaq1'))

        #valid input
        self.assertTrue(validate_pass(valid_pass, valid_pass))

if __name__ == "__main__":
    unittest.main() # run all tests
