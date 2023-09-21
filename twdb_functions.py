import sqlite3

def enable_foreign_keys(connection):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.close()

def setup_database():
    # Connect to the database (this will create a new .db file if it doesn't exist)
    conn = sqlite3.connect('twitter_data.db')
    enable_foreign_keys(conn)
    cursor = conn.cursor()

    # Create TwitterAccounts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TwitterAccounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        following_count INTEGER
    )
    ''')

    # Create Followings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Followings (
        following_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        following_username TEXT NOT NULL,
        FOREIGN KEY (account_id) REFERENCES TwitterAccounts(account_id)
    )
    ''')

    #Commit changes and close the connection
    conn.commit()
    conn.close()


def insert_twitter_account(username, following_count):
    conn = sqlite3.connect('twitter_data.db')
    enable_foreign_keys(conn)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR IGNORE INTO TwitterAccounts (username, following_count) VALUES (?, ?)
    ''', (username, following_count))
    
    cursor.execute('''
    SELECT account_id FROM TwitterAccounts WHERE username = ?
    ''', (username,))
    account_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()
    return account_id

def insert_following(account_id, following_username):
    conn = sqlite3.connect('twitter_data.db')
    enable_foreign_keys(conn)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Followings (account_id, following_username) VALUES (?, ?)
    ''', (account_id, following_username))

    conn.commit()
    conn.close()