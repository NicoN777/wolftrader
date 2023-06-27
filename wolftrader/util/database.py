import sqlite3
from application import database_name, database_password, database_username, database_settings, azure_connection_string
import pyodbc
from util.logger import *
from util.handler import exception

class DBFactory:
    def __init__(self, kind='sqlite'):
        if kind is None:
            raise ValueError('Must specify a kind of connection')
        self.kind = kind
        self.db = None

    def get_db(self):
        if self.kind == 'AzureSQLServer':
            self.db = SQLServerUtil
        if self.kind == 'sqlite':
            self.db = SQLiteUtil
        return self.db()


class Base:
    def __init__(self, user=None, password=None, host=None, port=None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    @exception
    def read(self, query, tracker, param=None):
        if not param:
            result = self.cursor.execute(query)
        else:
            result = self.cursor.execute(query, param)
        column_names = list(map(lambda x:x[0], result.description))
        data = {'column_names': column_names, 'records': result.fetchall()}
        log_debug(f'{tracker}, SQL = {query}, executed successfully')
        return data

    @exception
    def write(self, statement, record, tracker):
        result = self.cursor.execute(statement, record)
        log_debug(f'{tracker} successful, SQL = {statement} | record = {record} ')

    @exception
    def write_many(self, statement, records, tracker):
        result = self.cursor.executemany(statement, records)
        log_debug(f'{tracker} successful, SQL = {statement} | record = {records} ')
        log_info(f'{tracker} successful, SQL = {statement}')

    @exception
    def close_connection(self):
        log_debug('Closing connection to database: {} ...'.format(self.db_name))
        self.connection.close()
        log_debug('Connection closed!')

    def __repr__(self):
        return str(self.__dict__)


class SQLServerUtil(Base):
    from application import azure_connection_string
    def __init__(self):
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
            log_debug('{} | Connection to database {}, successful.'.format(SQLiteUtil.class_name, SQLiteUtil.db_name))
        except Exception as error:
            log_critical('{} | Connection has failed, Error: {}'.format(SQLiteUtil.class_name, error))

    def __repr__(self):
        return 'SQLiteUtil() initialization variables are read from wolfie.ini file.'

    def __str__(self):
        return '----> Database Name: {}'.format(SQLiteUtil.db_name)

