import sqlite3
from util.logger import *
from application import database_name, database_password, database_username, database_settings

class DatabaseUtil:

    class_name =  __file__

    def __init__(self):
        try:
            DatabaseUtil.db_name = database_name.split('/')[-1]
            DatabaseUtil.connection = sqlite3.connect(database_name, isolation_level=None)
            DatabaseUtil.cursor = DatabaseUtil.connection.cursor()
            log_info('{} | Connection to database {}, successfull.'.format(DatabaseUtil.class_name, DatabaseUtil.db_name))
        except Exception as error:
            log_critical('{} | Connection has failed, Error: {}'.format(DatabaseUtil.class_name, error))

    def close_connection(self):
        try:
            log_info('Closing connection to database: {} ...'.format(DatabaseUtil.db_name))
            DatabaseUtil.connection.close()
            log_info('Connection closed!')
        except Exception as error:
            log_critical('Error closing database connection, Error: {}'.format(error))

    def __repr__(self):
        return 'DatabaseUtil() initialization variables are read from application.properties file.'

    def __str__(self):
        return '----> Database Name: {}'.format(DatabaseUtil.db_name)