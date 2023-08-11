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

insert_ban_users_count = '''INSERT OR IGNORE INTO users_ban VALUES (?,?,?)'''
insert_users = 'INSERT OR IGNORE INTO telegram_users VALUES (?,?,?,?,?)'
select_users_ban = '''SELECT Telegram_id FROM users_ban WHERE Telegram_id = (?)'''
update_users_ban_count=('''UPDATE users_ban SET BanCount = BanCount + 1 WHERE Telegram_id = (?)''')
select_users_counts = '''SELECT BanCount FROM users_ban WHERE Telegram_id = (?)'''
delete_banned_users = '''DELETE FROM users_ban WHERE Telegram_id = (?)'''
