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
        FOREIGN KEY (account_id) REFERENCES TwitterAccounts(account_id),
        UNIQUE(account_id, following_username)
    )
    ''')

    #Commit changes and close the connection
    conn.commit()
    conn.close()

#insert twitter account into TwitterAccounts - ignores duplicate entries.
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

#insert following account into followings column - ignores duplicate entries based on combo of account id and username
def insert_following(account_id, following_username):
    conn = sqlite3.connect('twitter_data.db')
    enable_foreign_keys(conn)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR IGNORE INTO Followings (account_id, following_username) VALUES (?, ?)
    ''', (account_id, following_username))

    conn.commit()
    conn.close()

# Check if new following count is greater than stored count, if it is then update the following_count
#  -> returns true, false or none
def check_following_count(username, new_count):
    conn = sqlite3.connect('twitter_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT following_count FROM TwitterAccounts WHERE username = ?
    ''', (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        current_count = result[0]
        if current_count == new_count:
            print(f"The following count for {username} matches the database.")
            return True
        else:
            print(f"Updating the following count for {username} in the database.")
            cursor.execute('''
            UPDATE TwitterAccounts SET following_count = ? WHERE username = ?
            ''', (new_count, username))
            conn.commit()
            return False
    else:
        print(f"No record found for username: {username}")
        return None

