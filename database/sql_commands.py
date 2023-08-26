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
        self.connection.execute(sql_queries.create_already_friend)
        self.connection.execute(sql_queries.create_reference_list)
        self.connection.execute(sql_queries.create_balance_user_reference)
        self.connection.execute(sql_queries.create_transactions_table)
        self.connection.execute(sql_queries.create_news_table)
        self.connection.execute(sql_queries.create_favorite_news_table)
        self.connection.commit()

    def insert_table(self, telegram_id, username, firstname, lastname):
        self.cursor.execute(sql_queries.insert_telegram_users,
                            (None, telegram_id, username, firstname, lastname,None)
                            )
        self.connection.commit()

    def insert_ban_users_count(self, telegram_id, bancount):
        self.cursor.execute(sql_queries.insert_users_ban,
                            (None, telegram_id, bancount)
                            )
        self.connection.commit()

    def select_users_ban(self, telegram_id):
        return self.cursor.execute(sql_queries.select_users_ban,
                                   (telegram_id,)
                                   ).fetchone()

    def update_ban_users_count(self, telegram_id):
        self.cursor.execute(sql_queries.update_users_ban,
                            (telegram_id,)
                            )
        self.connection.commit()

    def select_users_counts(self, telegram_id):
        return self.cursor.execute(sql_queries.select_BanCount,
                                   (telegram_id,)
                                   ).fetchone()

    def delete_banned_users(self, telegram_id):
        self.cursor.execute(sql_queries.delete_banned_users,
                            (telegram_id,)
                            )
        self.connection.commit()

    def select_users_for_admin(self):
        self.cursor.row_factory = lambda cursor, row: {
            'telegram_id': row[0],
            "username": row[1],
            "firstname": row[2]
        }
        return self.cursor.execute(sql_queries.select_users_for_admin).fetchall()

    def select_potential_ban_users(self):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id": row[0],
            "username": row[1],
            "firstname": row[2],
            "Bancount": row[3]
        }
        return self.cursor.execute(sql_queries.select_potential_ban_users).fetchall()

    def select_all_users(self):
        self.cursor.row_factory = lambda cursor, row: {
            'telegram_id': row[0]
        }
        return self.cursor.execute(sql_queries.select_telegram_id_from_tg_users).fetchall()

    def sql_insert_user_info(self, telegram_id, name_of_user, age, bio, photo):
        self.connection.execute(sql_queries.insert_user_info, (None, telegram_id, name_of_user,
                                                               age, bio, photo))
        self.connection.commit()

    def sql_select_user_info(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "name": row[0],
            "age": row[1],
            "bio": row[2],
            'photo': row[3],

        }
        return self.cursor.execute(sql_queries.select_users_info, (telegram_id,)).fetchall()

    def sql_insert_poll_answers(self, idea, problems, telegram_id):
        self.cursor.execute(sql_queries.insert_poll,
                            (None, idea, problems, telegram_id)
                            )
        self.connection.commit()

    def sql_select_poll_answers_by_id(self, id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "idea": row[1],
            "problems": row[2],
            'telegram_id': row[3],

        }
        return self.cursor.execute(sql_queries.select_poll_answers_by_id, (id,)).fetchall()

    def sql_select_all_poll_answers_id(self):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
        }
        return self.cursor.execute(sql_queries.sql_select_all_poll_answers_id).fetchall()

    def sql_insert_into_adminrate(self, admin_telegram_id, telegram_id, rating):
        self.cursor.execute(sql_queries.insert_into_adminrating,
                            (None, admin_telegram_id, telegram_id, rating)
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

    def sql_select_tg_user_by_username(self, username):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id": row[0],
        }
        return self.cursor.execute(sql_queries.select_telegram_users_by_username, (username,)).fetchall()

    def sql_insert_user_complain(self, username_first_who_complained, telegram_id_complained_user, telegram_id_bad_user,
                                 reason, count):
        self.cursor.execute(sql_queries.insert_user_complain,
                            (None, username_first_who_complained, telegram_id_complained_user, telegram_id_bad_user,
                             reason, count)
                            )
        self.connection.commit()

    def sql_select_existing_bad_user(self, telegram_id_bad_user):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id_bad_user": row[0],
        }
        return self.cursor.execute(sql_queries.select_existing_bad_user, (telegram_id_bad_user,)).fetchall()

    def sql_update_user_complain(self, telegram_id_bad_user):
        self.cursor.execute(sql_queries.update_user_complain, (telegram_id_bad_user,))
        self.connection.commit()

    def sql_select_report_count(self, telegram_id_bad_user):
        self.cursor.row_factory = lambda cursor, row: {
            'report_count': row[0],
        }
        return self.cursor.execute(sql_queries.select_report_count, (telegram_id_bad_user,)).fetchall()

    def sql_delete_reported_banned_users(self, telegram_id_bad_user):
        self.cursor.execute(sql_queries.delete_reported_banned_users,
                            (telegram_id_bad_user,)
                            )
        self.connection.commit()

    def sql_select_username_who_reported(self, username_who_reported):
        self.cursor.row_factory = lambda cursor, row: {
            'username_who_reported': row[0],
            'telegram_id_complained': row[1],
            'telegram_id_bad_user': row[2]
        }
        return self.cursor.execute(sql_queries.select_username_who_reported, (username_who_reported,)).fetchall()

    def sql_update_report_count(self, username_who_reported, telegram_id_complained_user, telegram_id_bad_user):
        self.cursor.execute(sql_queries.update_report_count,
                            (username_who_reported, telegram_id_complained_user, telegram_id_bad_user))
        self.connection.commit()

    def sql_select_tg_user_by_firstname(self, firstname):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id": row[0],
        }
        return self.cursor.execute(sql_queries.select_telegram_users_by_firstname, (firstname,)).fetchall()

    def sql_select_all_user_complain(self):
        self.cursor.row_factory = lambda cursor, row: {
            "ID" : row[0],
            "who_complained": row[1],
            "tg_id_complained_user": row[2],
            "tg_id_bad_user": row[3],
            "reason": row[4],
            "count": row[5]
        }
        return self.cursor.execute(sql_queries.select_all_user_complain).fetchall()

    def sql_insert_already_friend(self,owner_id,friended_tg_id):
        self.cursor.execute(sql_queries.sql_insert_already_friend,
                            (owner_id, friended_tg_id)
                            )
        self.connection.commit()

    def sql_select_already_friend(self,owner_id,friended_tg_id):
        self.cursor.row_factory = lambda cursor, row: {
            "owner_id": row[0],
            "friended_tg_id": row[1],
        }
        return self.cursor.execute(sql_queries.sql_select_already_friend,(owner_id,friended_tg_id)).fetchall()

    def update_report_count_by_friend(self,ID):
        self.cursor.execute(sql_queries.update_report_count_by_friend,
                            (ID,))
        self.connection.commit()

    def delete_user_complain(self):
        self.cursor.execute(sql_queries.delete_user_complain)
        self.connection.commit()

    def sql_select_existed_link(self,telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "link": row[0],
        }
        return self.cursor.execute(sql_queries.sql_select_existed_link,(telegram_id,)).fetchall()

    def sql_update_telegram_user_link(self,reference_link,telegram_id):
        self.cursor.execute(sql_queries.update_telegram_user_link,
                            (reference_link, telegram_id))
        self.connection.commit()

    def sql_select_owner_user_by_link(self,link):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id": row[0],
        }
        return self.cursor.execute(sql_queries.select_owner_user_by_link,(link,)).fetchall()


    def sql_insert_reference_list(self, owner_tg_id, reference_tg_id):
        self.cursor.execute(sql_queries.sql_insert_reference_list,
                            (None,owner_tg_id, reference_tg_id)
                            )
        self.connection.commit()

    def sql_select_reference_users_by_owner_tg_id(self,owner_tg_id):
        self.cursor.row_factory = lambda cursor, row: {
            "referral_telegram_id": row[0],
        }
        return self.cursor.execute(sql_queries.sql_select_reference_users_by_owner_tg_id, (owner_tg_id,)).fetchall()

    def sql_insert_into_balance(self,telegram_id,balance):
        self.cursor.execute(sql_queries.insert_into_balance,
                            (None, telegram_id,balance)
                            )
        self.connection.commit()

    def sql_select_reference_tg_id(self,referral_telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "referral_telegram_id": row[0],
        }
        return self.cursor.execute(sql_queries.select_reference_tg_id, (referral_telegram_id,)).fetchall()

    def update_balance(self,telegram_id):
        self.cursor.execute(sql_queries.update_balance,
                            (telegram_id,))
        self.connection.commit()

    def select_existing_balance(self,telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id": row[0],
        }
        return self.cursor.execute(sql_queries.select_existing_balance, (telegram_id,)).fetchall()

    def sql_select_my_balance(self,telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "balance": row[0],
        }
        return self.cursor.execute(sql_queries.sql_select_my_balance_by_id, (telegram_id,)).fetchall()

    def sql_select_users_balance_by_user_firsname(self,username,firstname):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id": row[0],
        }
        return self.cursor.execute(sql_queries.sql_select_users_balance_by_user_firsname, (username,firstname)).fetchall()

    def sql_update_sender_balance(self,balance,telegram_id):
        self.cursor.execute(sql_queries.sql_update_sender_balance,
                            (balance,telegram_id))
        self.connection.commit()


    def sql_update_balance_recipient_balance(self,balance,telegram_id):
        self.cursor.execute(sql_queries.sql_update_balance_recipient_balance,
                            (balance,telegram_id))
        self.connection.commit()

    def sql_select_into_transactions(self,Sender_id,Recipient_id,Amount):
        self.cursor.execute(sql_queries.sql_select_into_transactions,
                            (None, Sender_id, Recipient_id,Amount)
                            )
        self.connection.commit()


    def sql_insert_news(self,news):
        self.cursor.execute(sql_queries.sql_insert_news_table,
                            (None,news)
                            )
        self.connection.commit()


    def sql_insert_favorite_news(self,telegram_id,favorite_news):
        self.cursor.execute(sql_queries.sql_insert_favorite_news_table,
                            (None, telegram_id,favorite_news)
                            )
        self.connection.commit()

    def sql_select_news_id_by_link(self,news):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
        }
        return self.cursor.execute(sql_queries.sql_select_news_id_by_link,
                                   (news,)).fetchall()

    def sql_select_news_link_by_id(self,id):
        self.cursor.row_factory = lambda cursor, row: {
            "news": row[0],
        }
        return self.cursor.execute(sql_queries.sql_select_news_link_by_id,
                                   (id,)).fetchall()


    def sql_select_favorite_news_by_own_id(self,telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "favorite_news": row[0],
        }
        return self.cursor.execute(sql_queries.select_favorite_news_by_own_id,
                                   (telegram_id,)).fetchall()


    def sql_select_my_favorite_news_id_by_link(self,link):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
        }
        return self.cursor.execute(sql_queries.select_my_favorite_news_id_by_link,
                                   (link,)).fetchall()


    def sql_delete_from_favorite_news(self,id):
        self.cursor.execute(sql_queries.delete_from_favorite_news,
                            (id,)
                            )
        self.connection.commit()




