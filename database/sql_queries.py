create_user_table = """
        CREATE TABLE IF NOT EXISTS telegram_users
        (Id INTEGER PRIMARY KEY,
        Telegram_id INTEGER,
        Username CHAR(50),
        Firstname CHAR(50),
        Lastname CHAR(50),
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

update_report_count = '''UPDATE user_complain SET REPORT_COUNT = REPORT_COUNT - 1 WHERE TELEGRAM_USERNAME_FIRST_COMPLAINED = (?) AND 
                        TELEGRAM_ID_COMPLAINED_USER = (?) AND TELEGRAM_ID_BAD_USER = (?)'''

select_username_who_reported = 'SELECT TELEGRAM_USERNAME_FIRST_COMPLAINED,TELEGRAM_ID_COMPLAINED_USER,TELEGRAM_ID_BAD_USER FROM user_complain WHERE TELEGRAM_USERNAME_FIRST_COMPLAINED = (?)'

delete_reported_banned_users = '''DELETE FROM user_complain WHERE TELEGRAM_ID_BAD_USER = (?)'''

select_report_count = '''SELECT REPORT_COUNT FROM user_complain WHERE TELEGRAM_ID_BAD_USER = (?)'''

select_existing_bad_user = '''SELECT TELEGRAM_ID_BAD_USER FROM user_complain WHERE TELEGRAM_ID_BAD_USER = ?'''

select_telegram_users_by_username = '''SELECT telegram_id FROM telegram_users WHERE Username = ?'''

insert_user_complain = '''INSERT OR IGNORE INTO user_complain VALUES (?,?,?,?,?,?)'''

update_user_complain = '''UPDATE user_complain SET REPORT_COUNT = REPORT_COUNT + 1 WHERE TELEGRAM_ID_BAD_USER = (?)'''

select_users_info = '''SELECT name_of_user,age,bio,photo FROM user_info WHERE Telegram_id = ?'''

insert_user_info = '''INSERT OR IGNORE INTO user_info VALUES (?,?,?,?,?,?)'''

insert_users_ban = '''INSERT OR IGNORE INTO users_ban VALUES (?,?,?)'''

insert_telegram_users = 'INSERT OR IGNORE INTO telegram_users VALUES (?,?,?,?,?)'

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

