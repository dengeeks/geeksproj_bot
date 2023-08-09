import sqlite3

from database import sql_queries


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('hw1.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        if self.connection:
            print('Database connected successfully')
        self.connection.execute(sql_queries.create_user_table)
        self.connection.commit()

    def insert_table(self, telegram_id, username, firstname, lastname):
        self.cursor.execute(sql_queries.insert_users,
                            (None, telegram_id, username, firstname, lastname)
                            )
        self.connection.commit()
