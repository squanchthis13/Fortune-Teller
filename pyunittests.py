'''PyUnit tests to test input validation methods/logic'''
import unittest
from databasehelper import *

class InvalidStrngTest(unittest.TestCase):

    def setUp(self):
        '''Call before every test case'''
        #invalid inputs for uname, fname, lname
        self.blank_input = ''
        self.spec_char_input = 'te$t'
        self.num_input = 't3st'
        self.too_long_input = 'TestInputTooLongTest'

        #valid inputs for email, password
        self.email = 'test@test.com'
        self.pass1 = '1qaz!QAZ2wsx@WSX'
        self.pass2 = '1qaz!QAZ2wsx@WSX'

    #@unittest.expectedFailure
    def test_validate_string(self):
        self.assertFalse(validate_string(self.blank_input))
        self.assertFalse(validate_string(self.spec_char_input))
        
        # update dbhelper.py input validation to check against num input
        # expectedFailure
        self.assertFalse(validate_string(self.num_input))

        self.assertFalse(validate_string(self.spec_char_input))

    def test_username_exists(self):
        self.assertFalse(check_username_exists(self.blank_input))

if __name__ == "__main__":
    unittest.main() # run all tests
