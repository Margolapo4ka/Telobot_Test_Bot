import sqlite3
# try:
#     sqlite_connection = sqlite3.connect('user_telebot.db')
#     cursor = sqlite_connection.cursor()
#     sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS users (
#                                     name TEXT ,
#                                     surname text ,
#                                     age integer );'''
#
#     name = 'Марго'
#     surname = 'Шварц'
#     age = '20'
#     sqlite_select_query = 'INSERT INTO users (name, surname, age) VALUES ( ' + '\'' + name + '\',' + ' \'' + surname + '\', ' + age + ');'
#     cursor.execute(sqlite_select_query)
#     sqlite_output = 'SELECT * FROM users;'
#     cursor.execute(sqlite_output)
#     record = cursor.fetchall()
#     print(record)
# except sqlite3.Error as error:
#     print(error)

class SQLite:

    def __init__(self, name_db):
        self.__connection = sqlite3.connect(name_db, check_same_thread=False)
        self.__cursor = self.__connection.cursor()

    def close(self):
        self.__connection.close()

    def execute(self, command):
        try:
            self.__cursor.execute(command)
            self.__connection.commit()
            return True
        except sqlite3.Error as error:
            print(error)
            return False

    def select_execute(self):
        try:
            sqlite_output = 'SELECT * FROM users;'
            self.__cursor.execute(sqlite_output)
            record = self.__cursor.fetchall()
            print(record)
            return record


        except sqlite3.Error as error:
            print(error)


    def del_execut(self, user_id):
        try:
            sqlite_select_del = 'DELETE FROM users WHERE id=' + str(user_id) + ';'
            self.__cursor.execute(sqlite_select_del)
            self.__connection.commit()
            return True

        except sqlite3.Error as error:
            print(error)
            return False


    def add_admin_execut(self, id_admin, name):
        try:
            sqlite_select_admin = 'INSERT INTO admin (id, name) VALUES ( ' + str(id_admin) + ', \'' + name + '\'' ');'
            self.__cursor.execute(sqlite_select_admin)
            self.__connection.commit()
            return True

        except sqlite3.Error as error:
            print(error)
            return False

    def check_admin_execut(self, id_admin):
        try:
            sqlite_check_admin = 'SELECT * FROM admin WHERE id in (' + str(id_admin) + ');'
            self.__cursor.execute(sqlite_check_admin)
            return True
        except sqlite3.Error as error:
            print(error)
            return False

    def del_admin_execut(self, id_admin):
        try:
            sqlite_select_del_admin = 'DELETE FROM admin WHERE id=' + str(id_admin) + ';'
            self.__cursor.execute(sqlite_select_del_admin)
            self.__connection.commit()
            return True

        except sqlite3.Error as error:
            print(error)
            return False

    def list_admin_execut(self):
        sqlite_output = 'SELECT * FROM admin;'
        self.__cursor.execute(sqlite_output)
        record = self.__cursor.fetchall()
        print(record)
        return record



# try:
#
#     # sqlite_connection = sqlite3.connect('user_telebot.db', check_same_thread=False)
#     # cursor = connection.cursor()
#     sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS users (
#                                         id integer,
#                                         name TEXT ,
#                                         surname text ,
#                                         age integer );'''
#     cursor.execute(sqlite_create_table_query)
#
#
# except sqlite3.Error as error:
#     print(error)
#
# def add_user(user_id, name, surname, age):
#     try:
#
#         sqlite_select_query = 'INSERT INTO users (id, name, surname, age) VALUES ( ' + str(user_id) + ', \'' + name + '\',' + ' \'' + surname + '\', ' + age + ');'
#         cursor.execute(sqlite_select_query)
#         sqlite_connection.commit()
#         return True
#
#     except sqlite3.Error as error:
#         print(error)
#         return False
#
# def get_users_bd():
#     try:
#         sqlite_output = 'SELECT * FROM users;'
#         cursor.execute(sqlite_output)
#         record = cursor.fetchall()
#         print(record)
#         return record
#     except sqlite3.Error as error:
#         print(error)
#
# def del_user_bd(user_id):
#     try:
#         sqlite_select_del = 'DELETE FROM users WHERE id=' + str(user_id) + ';'
#         cursor.execute(sqlite_select_del)
#         sqlite_connection.commit()
#         return True
#
#     except sqlite3.Error as error:
#         print(error)
#         return False
#
