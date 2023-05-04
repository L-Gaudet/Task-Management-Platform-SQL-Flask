import mysql.connector

class db_operations: 
    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                                                user='root',
                                                password='cpsc408!',
                                                auth_plugin='mysql_native_password',
                                                database='TaskApp')

        # create cursor object
        self.cursor = self.connection.cursor()
        print('connection made...')

    def destroy(self):
        self.connection.close()
        self.cursor.close()

    def get_all_users(self):
        query = '''
        SELECT * 
        FROM users;
        '''
        self.cursor.execute(query)
        return self.cursor.fetchall()
