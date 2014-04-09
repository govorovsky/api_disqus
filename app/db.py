import MySQLdb
from config import *

class Database:
    connection = None

    def __init__(self):
        self.connect()

    def insert(self, query, data=None):
        try:
            cursor = self.get_cursor(query, data)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.get_cursor(query, data)
        self.connection.commit()
        cursor.close()

    def query(self, query, data=None):
        try:
            cursor = self.get_cursor(query, data)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.get_cursor(query, data)
        data = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return data

    def connect(self):
        self.connection = MySQLdb.connect(host, user, password, forum_db, use_unicode=True)
        self.connection.set_character_set('utf8')
        c = self.connection.cursor()
        c.execute('SET NAMES utf8;')
        c.close()

    def get_cursor(self, query, data=None):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        if data is None:
            cursor.execute(query)
        else:
            if type(data) is tuple:
                cursor.execute(query, data)
            else:
                cursor.execute(query, (data,))
        return cursor


db = Database()
