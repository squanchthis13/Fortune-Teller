'''PyUnit tests to test input validation methods/logic'''
import unittest
from databasehelper import check_email_exists, sign_up

class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        '''Call before every test case'''
        self.uname = 'USERNAME'
        self.fname = 'FirstName'
        self.lname = 'LastName'
        self.email = 'test@test.com'
        self.pass1 = '1qaz!QAZ2wsx@WSX'
        self.pass2 = '1qaz!QAZ2wsx@WSX'
    
    def testA(self):
        self.assertFalse(check_email_exists(self.email))
        

if __name__ == "__main__":
    unittest.main() # run all tests