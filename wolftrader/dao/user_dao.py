from wolftrader.util.logger import *
from wolftrader.util.database import DatabaseUtil

class UserDAO(DatabaseUtil):
    class_name = __file__

    def __init__(self):
        try:
            DatabaseUtil.__init__(self)
            log_info('{} | UserDAO has been initialized successfully'.format(UserDAO.class_name))
        except Exception as error:
            log_critical('{} | UserDAO initialization has failed. Error: {}'.format(UserDAO.class_name, error))

    def get_user_by_id(self, id):
        try:
            sql = 'SELECT NAME, EMAIL FROM USERS WHERE ID=?'
            cursor = DatabaseUtil.cursor.execute(sql, id)
            data = cursor.fetchall()
            log_info('{} | get_user_by_id successful, SQL={}'.format(UserDAO.class_name, sql))
            return data
        except Exception as error:
            log_critical('{} | get_user_by_id. Error: {}'.format(UserDAO.class_name, error))

    def get_user_emails(self):
        try:
            sql = 'SELECT EMAIL FROM USERS'
            cursor = DatabaseUtil.cursor.execute(sql)
            data = cursor.fetchall()
            log_info('{} | get_user_emails successful, SQL={} '.format(UserDAO.class_name, sql))
            print(data, type(data))
            return data
        except Exception as error:
            log_critical('{} | get_user_emails. Error: {}'.format(UserDAO.class_name, error))