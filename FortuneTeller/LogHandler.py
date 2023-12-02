'''
Created on Dec 2, 2023

@author: chelseanieves
'''
import logging
from logging import FileHandler
from logging import Formatter

#Create and modify logger
log_format = (
"%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
log_level = logging.INFO

# messaging logger
user_log_file = "./user_log.log"

user_logger = logging.getLogger("fortuneteller.user")
user_logger.setLevel(log_level)
user_logger_FH = FileHandler(user_log_file)
user_logger_FH.setLevel(log_level)
user_logger_FH.setFormatter(Formatter(log_format))
# add handler to user_logger
user_logger.addHandler(user_logger_FH)

# payments logger
db_log_file = "./db_log.log"
db_logger = logging.getLogger("wasted_meerkats.payments")

db_logger.setLevel(log_level)
db_logger_FH = FileHandler(db_log_file)
db_logger_FH.setLevel(log_level)
db_logger_FH.setFormatter(Formatter(log_format))
db_logger.addHandler(db_logger_FH)
    
    