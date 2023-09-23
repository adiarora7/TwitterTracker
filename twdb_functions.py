import sqlite3
from datetime import datetime
import smtplib
from email.message import EmailMessage

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
        display_name TEXT NOT NULL,
        following_count INTEGER
    )
    ''')

    # Create Followings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Followings (
        following_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        following_username TEXT NOT NULL,
        date_added TEXT NOT NULL,
        FOREIGN KEY (account_id) REFERENCES TwitterAccounts(account_id),
        UNIQUE(account_id, following_username)
    )
    ''')

    #Commit changes and close the connection
    conn.commit()
    conn.close()




#insert twitter account into TwitterAccounts - ignores duplicate entries.
def insert_twitter_account(username, display_name, following_count):
    conn = sqlite3.connect('twitter_data.db')
    enable_foreign_keys(conn)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR IGNORE INTO TwitterAccounts (username, display_name, following_count) VALUES (?, ?, ?)
    ''', (username, display_name, following_count))
    
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
    INSERT OR IGNORE INTO Followings (account_id, following_username, date_added) VALUES (?, ?, DATE('now'))
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



#grabs data as follows [[userA, userX], [userA, userY], [userB, userZ]] where [0] follows [1]
def get_todays_followings():
    conn = sqlite3.connect('twitter_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT ta.display_name, f.following_username 
    FROM Followings f
    JOIN TwitterAccounts ta ON f.account_id = ta.account_id
    WHERE f.date_added = DATE('now')
    ''')

    followings = cursor.fetchall()
    conn.close()

    return followings



#Takes data ^ and creates a dictionary, then formats data into message
def format_following_message():
    followings = get_todays_followings()
    if not followings:
        return "No new followings today."

    # Grouping by user
    grouped = {}
    for account, following in followings:
        if account not in grouped:
            grouped[account] = []
        grouped[account].append(following)

    # Formatting the message
    messages = []
    for account, follows in grouped.items():
        follow_string = '\n'+'\n'.join(follows)
        messages.append(f"{account} followed {follow_string}.")

    messages = '\n\n'.join(messages)
    current_date = datetime.now().strftime('%Y-%m-%d')
    final_message = (f"Hey Nikita, today \n\n"
                     f"{messages} \n\n"
                     f"Sent on {current_date} by Adi's Bot.")
    
    return final_message



def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'twleadbot@gmail.com'
    msg['To'] = 'adiarora710@gmail.com'

    # Establish a connection to the email server (replace this with your email provider's SMTP server and port)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('twleadbot@gmail.com', 'mewh fwhl bbpe uexx') 
    server.send_message(msg)
    server.quit()