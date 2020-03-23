import sqlite3
from application import database_name, database_password, database_username, database_settings, azure_connection_string
import pyodbc
from util.logger import *



class Base:
    def __init__(self, user=None, password=None, host=None, port=None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def read(self, query, tracker, param=None):
        try:
            if not param:
                result = self.cursor.execute(query)
            else:
                result = self.cursor.execute(query, param)
            column_names = list(map(lambda x:x[0], result.description))
            data = {'column_names': column_names, 'records': result.fetchall()}
            log_info(f'{tracker}, SQL = {query}, executed successfully')
            return data
        except Exception as e:
            log_critical(f'{tracker} error while executing {query}\n Error: {e}')

    def write(self, statement, record, tracker):
        try:
            result = self.cursor.execute(statement, record)
            log_info(f'{tracker} successful, SQL = {statement} | record = {record} ')
        except Exception as e:
            log_critical(f'{tracker} error while executing {statement}\n Error: {e}')

    def write_many(self, statement, records, tracker):
        try:
            result = self.cursor.executemany(statement, records)
            log_info(f'{tracker} successful, SQL = {statement} | record = {records} ')
        except Exception as e:
            log_critical(f'{tracker} error while executing {statement}\n Error: {e}')

    def close_connection(self):
        try:
            log_info('Closing connection to database: {} ...'.format(self.db_name))
            self.connection.close()
            log_info('Connection closed!')
        except Exception as error:
            log_critical('Error closing database connection, Error: {}'.format(error))

    def __repr__(self):
        return str(self.__dict__)

class SQLServerUtil(Base):
    from application import azure_connection_string
    def __init__(self):
        print('mhm')
        SQLServerUtil.connection = pyodbc.connect(azure_connection_string, autocommit=True)

        SQLServerUtil.cursor = self.connection.cursor()

    def read(self, query, tracker, param=None):
        data = super().read(query, tracker, param)
        data['records'] = [tuple(_) for _ in data['records']]
        return data



class SQLiteUtil(Base):
    class_name = __file__

    def __init__(self):

        try:
            SQLiteUtil.db_name = database_name.split('/')[-1]
            SQLiteUtil.connection = sqlite3.connect(database_name, isolation_level=None)
            SQLiteUtil.cursor = SQLiteUtil.connection.cursor()
            log_info('{} | Connection to database {}, successfull.'.format(SQLiteUtil.class_name, SQLiteUtil.db_name))
        except Exception as error:
            log_critical('{} | Connection has failed, Error: {}'.format(SQLiteUtil.class_name, error))

    def __repr__(self):
        return 'SQLiteUtil() initialization variables are read from application.properties file.'

    def __str__(self):
        return '----> Database Name: {}'.format(SQLiteUtil.db_name)
