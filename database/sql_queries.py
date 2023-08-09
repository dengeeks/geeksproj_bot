create_user_table = """
        CREATE TABLE IF NOT EXISTS telegram_users
        (Id INTEGER PRIMARY KEY,
        Telegram_id INTEGER,
        Username CHAR(50),
        Firstname CHAR(50),
        Lastname CHAR(50)
        )
"""


insert_users = 'INSERT OR IGNORE INTO telegram_users VALUES (?,?,?,?,?)'