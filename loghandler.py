'''
Module to handle the creation and formatting of user and database loggers
modified 9Dec23
@author: Chelsea Nieves
'''
import logging
from logging import FileHandler
from logging import Formatter

# Create format for logged message
log_format = (
'%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d')
# Assign default logging level
log_level = logging.INFO

# User Logger
# create pathname to store log file
user_log_file = './user_log.log'
# Create logger
user_logger = logging.getLogger('fortuneteller.user')
# Assign default log level to logger
user_logger.setLevel(log_level)
# Create file handler
user_logger_FH = FileHandler(user_log_file)
# Assign log level to file handler
user_logger_FH.setLevel(log_level)
# Apply formatting to file handler
user_logger_FH.setFormatter(Formatter(log_format))
# Add handler to user_logger
user_logger.addHandler(user_logger_FH)

# DB Logger
# Create pathname to store log file
db_log_file = './db_log.log'
# Create logger
db_logger = logging.getLogger('fortuneteller.db')
# Set level to logger
db_logger.setLevel(log_level)
# Create file handler
db_logger_FH = FileHandler(db_log_file)
# Set level to file handler
db_logger_FH.setLevel(log_level)
# Apply formatting to file handler
db_logger_FH.setFormatter(Formatter(log_format))
# Add handler to db_logger
db_logger.addHandler(db_logger_FH)
