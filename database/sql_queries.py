create_user_table = """
        CREATE TABLE IF NOT EXISTS telegram_users
        (Id INTEGER PRIMARY KEY,
        Telegram_id INTEGER,
        Username CHAR(50),
        Firstname CHAR(50),
        Lastname CHAR(50),
        Reference_link TEXT NULL,
        UNIQUE (Telegram_id))
"""
create_ban_table = '''
        CREATE TABLE IF NOT EXISTS users_ban
        (Id INTEGER PRIMARY KEY,
        Telegram_id INTEGER,
        BanCount INTEGER,
        FOREIGN KEY (Telegram_id) REFERENCES telegram_users(Telegram_id))
'''

create_user_info_table = '''
CREATE TABLE IF NOT EXISTS user_info
        (Id INTEGER PRIMARY KEY,
        Telegram_id INTEGER,
        name_of_user CHAR(50),
        Age INTEGER,
        Bio CHAR(50),
        Photo TEXT,
        UNIQUE (Telegram_id))'''

create_poll_table = '''CREATE TABLE IF NOT EXISTS poll
                    (ID INTEGER PRIMARY KEY,
                    IDEA TEXT,
                    PROBLEMS TEXT,
                    TELEGRAM_ID INTEGER UNIQUE,
                    FOREIGN KEY (TELEGRAM_ID) REFERENCES user_info(TELEGRAM_ID))'''

create_admin_rating_table = '''CREATE TABLE IF NOT EXISTS admin_rating
                            (id INTEGER PRIMARY KEY,
                            admin_telegram_id INTEGER,
                            telegram_id INTEGER,
                            rating INTEGER,
                            UNIQUE (telegram_id),
                            FOREIGN KEY (TELEGRAM_ID) REFERENCES poll(TELEGRAM_ID),
                            FOREIGN KEY (admin_telegram_id) REFERENCES admin_list(admin_telegram_id))'''

create_admin_table = '''CREATE TABLE IF NOT EXISTS admin_list
                    (id INTEGER PRIMARY KEY,
                    admin_telegram_id INTEGER UNIQUE
                    )'''

create_report_users_table = '''CREATE TABLE IF NOT EXISTS user_complain
        (ID INTEGER PRIMARY KEY,
        TELEGRAM_USERNAME_FIRST_COMPLAINED CHAR(50),
        TELEGRAM_ID_COMPLAINED_USER INTEGER,
        TELEGRAM_ID_BAD_USER INTEGER,
        REASON TEXT,
        REPORT_COUNT INTEGER
        )'''

create_already_friend = """
        CREATE TABLE IF NOT EXISTS already_friend
        (OWNER_ID INTEGER,
        FRIENDED_TELEGRAM_ID INTEGER
        )
"""

create_reference_list = """
        CREATE TABLE IF NOT EXISTS reference_list
        (ID INTEGER PRIMARY KEY,
        OWNER_TELEGRAM_ID INTEGER,
        REFERENCE_TELEGRAM_ID INTEGER
        )
"""

create_balance_user_reference = '''CREATE TABLE IF NOT EXISTS balance
                                (ID INTEGER PRIMARY KEY,
                                telegram_id INTEGER,
                                balance INTEGER
                                )
'''

create_transactions_table = '''CREATE TABLE IF NOT EXISTS transactions
                            (ID INTEGER PRIMARY KEY,
                            Sender_id INTEGER,
                            Recipient_id INTEGER,
                            Amount INTEGER
                            )'''

sql_select_users_balance_by_user_firsname = '''SELECT telegram_id FROM balance WHERE telegram_id IN (
                                            SELECT telegram_id FROM telegram_users
                                            WHERE Username = ? OR firstname = ?
                                            )'''

sql_select_into_transactions = '''INSERT OR IGNORE INTO transactions VALUES(?,?,?,?)'''

sql_update_sender_balance = '''UPDATE balance SET balance = balance - (?) WHERE telegram_id = ?'''

sql_update_balance_recipient_balance = '''UPDATE balance SET balance = balance + (?) WHERE telegram_id = ?'''

sql_select_my_balance_by_id = '''SELECT balance FROM balance WHERE telegram_id = ?'''

select_existing_balance = '''SELECT telegram_id FROM balance WHERE telegram_id = ?'''

update_balance = '''UPDATE balance SET balance = balance + 100 WHERE telegram_id = ?'''

select_reference_tg_id = 'SELECT REFERENCE_TELEGRAM_ID FROM reference_list WHERE REFERENCE_TELEGRAM_ID = ?'

insert_into_balance = '''INSERT OR IGNORE INTO balance VALUES(?,?,?)'''

sql_select_reference_users_by_owner_tg_id = 'SELECT REFERENCE_TELEGRAM_ID FROM reference_list WHERE OWNER_TELEGRAM_ID = ?'

sql_insert_reference_list = '''INSERT OR IGNORE INTO reference_list VALUES(?,?,?)'''

select_owner_user_by_link = '''SELECT Telegram_id FROM telegram_users WHERE Reference_link = ?'''

update_telegram_user_link = '''UPDATE telegram_users SET Reference_link = ? WHERE telegram_id = ?'''

sql_select_existed_link = '''SELECT Reference_link FROM telegram_users WHERE Telegram_id = ?'''

sql_select_already_friend = '''SELECT OWNER_ID,FRIENDED_TELEGRAM_ID FROM already_friend WHERE OWNER_ID = ? AND FRIENDED_TELEGRAM_ID = (?)'''

delete_user_complain = '''DELETE FROM user_complain WHERE REPORT_COUNT = 0'''

sql_insert_already_friend = '''INSERT OR IGNORE INTO already_friend VALUES (?,?)'''

select_all_user_complain = '''SELECT ID,TELEGRAM_USERNAME_FIRST_COMPLAINED,TELEGRAM_ID_COMPLAINED_USER,
                            TELEGRAM_ID_BAD_USER,REASON,REPORT_COUNT FROM user_complain'''

update_report_count = '''UPDATE user_complain SET REPORT_COUNT = REPORT_COUNT - 1 WHERE TELEGRAM_USERNAME_FIRST_COMPLAINED = (?) AND 
                        TELEGRAM_ID_COMPLAINED_USER = (?) AND TELEGRAM_ID_BAD_USER = (?)'''

update_report_count_by_friend = '''UPDATE user_complain SET REPORT_COUNT = REPORT_COUNT - 1 WHERE ID = ?'''

select_username_who_reported = 'SELECT TELEGRAM_USERNAME_FIRST_COMPLAINED,TELEGRAM_ID_COMPLAINED_USER,TELEGRAM_ID_BAD_USER FROM user_complain WHERE TELEGRAM_USERNAME_FIRST_COMPLAINED = (?)'

delete_reported_banned_users = '''DELETE FROM user_complain WHERE TELEGRAM_ID_BAD_USER = (?)'''

select_report_count = '''SELECT REPORT_COUNT FROM user_complain WHERE TELEGRAM_ID_BAD_USER = (?)'''

select_existing_bad_user = '''SELECT TELEGRAM_ID_BAD_USER FROM user_complain WHERE TELEGRAM_ID_BAD_USER = ?'''

select_telegram_users_by_username = '''SELECT telegram_id FROM telegram_users WHERE Username = ?'''

select_telegram_users_by_firstname = '''SELECT telegram_id FROM telegram_users WHERE Firstname = ?'''

insert_user_complain = '''INSERT OR IGNORE INTO user_complain VALUES (?,?,?,?,?,?)'''

update_user_complain = '''UPDATE user_complain SET REPORT_COUNT = REPORT_COUNT + 1 WHERE TELEGRAM_ID_BAD_USER = (?)'''

select_users_info = '''SELECT name_of_user,age,bio,photo FROM user_info WHERE Telegram_id = ?'''

insert_user_info = '''INSERT OR IGNORE INTO user_info VALUES (?,?,?,?,?,?)'''

insert_users_ban = '''INSERT OR IGNORE INTO users_ban VALUES (?,?,?)'''

insert_telegram_users = 'INSERT OR IGNORE INTO telegram_users VALUES (?,?,?,?,?,?)'

select_users_ban = '''SELECT Telegram_id FROM users_ban WHERE Telegram_id = (?)'''

update_users_ban=('''UPDATE users_ban SET BanCount = BanCount + 1 WHERE Telegram_id = (?)''')

select_BanCount = '''SELECT BanCount FROM users_ban WHERE Telegram_id = (?)'''

delete_banned_users = '''DELETE FROM users_ban WHERE Telegram_id = (?)'''

select_users_for_admin = '''SELECT Telegram_id,Username,Firstname FROM telegram_users'''

select_potential_ban_users = '''SELECT telegram_users.Telegram_id,telegram_users.Username, telegram_users.Firstname,users_ban.BanCount FROM telegram_users 
                            JOIN users_ban ON telegram_users.Telegram_id = users_ban.Telegram_id'''

select_telegram_id_from_tg_users = '''SELECT Telegram_id FROM telegram_users'''

insert_poll = '''INSERT OR IGNORE INTO poll VALUES(?,?,?,?)'''

select_poll_answers_by_id = '''SELECT id,idea,problems,telegram_id FROM poll WHERE id = (?)'''

sql_select_all_poll_answers_id = '''SELECT id FROM poll'''

insert_into_adminrating = '''INSERT OR IGNORE INTO admin_rating VALUES(?,?,?,?)'''

select_admins_rating = '''SELECT admin_telegram_id,rating FROM admin_rating'''

select_admin_list = '''SELECT admin_telegram_id FROM admin_list'''

sql_select_avg_rating = '''SELECT admin_telegram_id,AVG(rating) FROM admin_rating GROUP BY admin_telegram_id'''

