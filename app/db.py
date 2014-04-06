from flaskext.mysql import MySQL
import MySQLdb
import sys


class Database:

    host = 'localhost'
    user = 'root'
    password = 'qazxsw12'
    db = 'mydb'
    connection = MySQLdb.connect(host, user, password, db)

    def insert(self, query, data=None):
        with Database.connection:
            cursor = self.connection.cursor()
            try:
                if data is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query,data)
                self.connection.commit()
            except:
                print "Unexpected error:", sys.exc_info()
                self.connection.rollback()
                cursor.close()
            cursor.close()

    def query(self, query, data=None):
        with Database.connection:
            cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
            if data is None:
                cursor.execute(query)
            else:
                cursor.execute(query,(data,))
            data = cursor.fetchall()
            cursor.close()
            return data



db = Database()
