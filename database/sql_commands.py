import sqlite3

from database import sql_queries


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('hw1.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        if self.connection:
            print('Database connected successfully')
        self.connection.execute(sql_queries.create_ban_table)
        self.connection.commit()

    def insert_table(self, telegram_id, username, firstname, lastname):
        self.cursor.execute(sql_queries.insert_users,
                            (None, telegram_id, username, firstname, lastname)
                            )
        self.connection.commit()

    def insert_ban_users_count(self,telegram_id,bancount):
        self.cursor.execute(sql_queries.insert_ban_users_count,
                            (None,telegram_id,bancount)
                            )
        self.connection.commit()

    def select_users_ban(self,telegram_id):
        return self.cursor.execute(sql_queries.select_users_ban,
                                   (telegram_id,)
                                   ).fetchone()

    def update_ban_users_count(self,telegram_id):
        self.cursor.execute(sql_queries.update_users_ban_count,
                            (telegram_id,)
                            )
        self.connection.commit()

    def select_users_counts(self,telegram_id):
        return self.cursor.execute(sql_queries.select_users_counts,
                                   (telegram_id,)
                                   ).fetchone()

    def delete_banned_users(self,telegram_id):
        self.cursor.execute(sql_queries.delete_banned_users,
                            (telegram_id,)
                            )
        self.connection.commit()

    def select_users_for_admin(self):
        self.cursor.row_factory = lambda cursor,row:{
            'telegram_id' : row[0],
            "username" : row[1],
            "firstname" : row[2]
        }
        return self.cursor.execute(sql_queries.select_users_for_admin).fetchall()

    def select_potential_ban_users(self):
        self.cursor.row_factory = lambda cursor,row:{
            "telegram_id" : row[0],
            "username" : row[1],
            "firstname" : row[2],
            "Bancount" : row[3]
        }
        return self.cursor.execute(sql_queries.select_potential_ban_users).fetchall()



    def select_all_users(self):
        self.cursor.row_factory = lambda cursor, row: {
            'telegram_id': row[0]
        }
        return self.cursor.execute(sql_queries.select_all_users).fetchall()

