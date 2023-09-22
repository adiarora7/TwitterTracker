import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from accounts_to_track import accounts_to_track
from twdb_functions import setup_database, insert_twitter_account, insert_following

#IMPORTANT LINKS
#https://twiteridfinder.com/
#https://github.com/vladkens/twscrape/blob/main/twscrape/



async def main():
    api = API()  # or API("path-to.db") - default is `accounts.db`
    # conn = sqlite3.connect('observers.db')
    # cur = conn.cursor()
    # await api.pool.add_account("berger_joe11181", "8Ct,m#9iZZY%St8", "lonestaraadi@gmail.com", "niggasinparis")
    # await api.pool.login_all()
  
    #USED TO INITIALIZE twitter_database.db
    setup_database()

    # get user by login
    user_login = "eladgil"
    await api.user_by_login(user_login)  # User

    # user info
    user_id = 6535212
    await api.user_by_id(user_id)  # User
    await gather(api.following(user_id, limit=10))  # list[User]
 
    #Create following list and get length -> following_number
    following_list = []
    async for user in api.following(user_id):
        following_list.append(user.username)

    # Insert user_login into the database and retrieve its account_id
    account_id = insert_twitter_account(user_login, len(following_list))

    # Insert every user from the following list into the database
    for username in following_list:
        insert_following(account_id, username)


if __name__ == "__main__":
    asyncio.run(main())