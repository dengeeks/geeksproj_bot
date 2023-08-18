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
        self.connection.execute(sql_queries.create_user_info_table)
        self.connection.execute(sql_queries.create_poll_table)
        self.connection.execute(sql_queries.create_admin_rating_table)
        self.connection.execute(sql_queries.create_admin_table)
        self.connection.execute(sql_queries.create_report_users_table)
        self.connection.commit()

    def insert_table(self, telegram_id, username, firstname, lastname):
        self.cursor.execute(sql_queries.insert_telegram_users,
                            (None, telegram_id, username, firstname, lastname)
                            )
        self.connection.commit()

    def insert_ban_users_count(self,telegram_id,bancount):
        self.cursor.execute(sql_queries.insert_users_ban,
                            (None,telegram_id,bancount)
                            )
        self.connection.commit()

    def select_users_ban(self,telegram_id):
        return self.cursor.execute(sql_queries.select_users_ban,
                                   (telegram_id,)
                                   ).fetchone()

    def update_ban_users_count(self,telegram_id):
        self.cursor.execute(sql_queries.update_users_ban,
                            (telegram_id,)
                            )
        self.connection.commit()

    def select_users_counts(self,telegram_id):
        return self.cursor.execute(sql_queries.select_BanCount,
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
        return self.cursor.execute(sql_queries.select_telegram_id_from_tg_users).fetchall()

    def sql_insert_user_info(self,telegram_id,name_of_user,age,bio,photo):
        self.connection.execute(sql_queries.insert_user_info,(None,telegram_id,name_of_user,
                                                              age,bio,photo))
        self.connection.commit()
    def sql_select_user_info(self,telegram_id):
        self.cursor.row_factory = lambda cursor,row:{
            "name" : row[0],
            "age" : row[1],
            "bio" : row[2],
            'photo': row[3],

        }
        return self.cursor.execute(sql_queries.select_users_info,(telegram_id,)).fetchall()

    def sql_insert_poll_answers(self, idea,problems,telegram_id):
        self.cursor.execute(sql_queries.insert_poll,
                            (None,idea,problems,telegram_id)
                            )
        self.connection.commit()

    def sql_select_poll_answers_by_id(self,id):
        self.cursor.row_factory = lambda cursor,row:{
            "id" : row[0],
            "idea" : row[1],
            "problems" : row[2],
            'telegram_id': row[3],

        }
        return self.cursor.execute(sql_queries.select_poll_answers_by_id,(id,)).fetchall()

    def sql_select_all_poll_answers_id(self):
        self.cursor.row_factory = lambda cursor,row:{
            "id" : row[0],
        }
        return self.cursor.execute(sql_queries.sql_select_all_poll_answers_id).fetchall()

    def sql_insert_into_adminrate(self,admin_telegram_id,telegram_id,rating):
        self.cursor.execute(sql_queries.insert_into_adminrating,
                            (None,admin_telegram_id,telegram_id,rating)
                            )
        self.connection.commit()

    def sql_select_admin_list(self):
        self.cursor.row_factory = lambda cursor, row: {
            "admin_tg_id": row[0],
        }
        return self.cursor.execute(sql_queries.select_admin_list).fetchall()

    def sql_select_admins_rating(self):
        self.cursor.row_factory = lambda cursor, row: {
            "admin_tg_id": row[0],
            "rating": row[1],
        }
        return self.cursor.execute(sql_queries.select_admins_rating).fetchall()

    def sql_avg_rating(self):
        self.cursor.row_factory = lambda cursor, row: {
            "admin_tg_id": row[0],
            "avg_rating": row[1],
        }
        return self.cursor.execute(sql_queries.sql_select_avg_rating).fetchall()


    def sql_select_tg_user_by_username(self,username):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id": row[0],
        }
        return self.cursor.execute(sql_queries.select_telegram_users_by_username,(username,)).fetchall()

    def sql_insert_user_complain(self,telegram_id_complained_user,telegram_id_bad_user,reason,count):
        self.cursor.execute(sql_queries.insert_user_complain,
                            (None,telegram_id_complained_user,telegram_id_bad_user,
                             reason,count)
                            )
        self.connection.commit()

    def sql_select_existing_bad_user(self,telegram_id_bad_user):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id_bad_user": row[0],
        }
        return self.cursor.execute(sql_queries.select_existing_bad_user, (telegram_id_bad_user,)).fetchall()


    def sql_update_user_complain(self,telegram_id_bad_user):
        self.cursor.execute(sql_queries.update_user_complain,(telegram_id_bad_user,))
        self.connection.commit()


    def sql_select_report_count(self,telegram_id_bad_user):
        self.cursor.row_factory = lambda cursor, row: {
            'report_count': row[0],
        }
        return self.cursor.execute(sql_queries.select_report_count,(telegram_id_bad_user,)).fetchall()

    def sql_delete_reported_banned_users(self,telegram_id_bad_user):
        self.cursor.execute(sql_queries.delete_reported_banned_users,
                            (telegram_id_bad_user,)
                            )
        self.connection.commit()

