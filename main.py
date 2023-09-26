import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from accounts_to_track import accounts_to_track, twitter_accounts
from twdb_functions import setup_database, insert_twitter_account, insert_following, check_following_count, format_following_message, send_email



#IMPORTANT LINKS
#https://twiteridfinder.com/
#https://github.com/vladkens/twscrape/blob/main/twscrape/

async def main():
    api = API()  # or API("path-to.db") - default is `accounts.db`

    # LOGIN
    # t = twitter_accounts

    # await api.pool.add_account("t[0][0]", "t[0][1]", "t[0][2]", "t[0][3]")
    # await api.pool.add_account(t[1][0], t[1][1], t[1][2], t[1][3])
    # await api.pool.login_all()
  
    #USED TO INITIALIZE twitter_database.db
    setup_database()

    for x in accounts_to_track:
        user_login, display_name, user_id = x

        # get user by login
        await api.user_by_login(user_login)  # User

        # user info
        await api.user_by_id(user_id)  # User
        await gather(api.following(user_id, limit=10))  # list[User]
 
        #Create following list and get length -> following_number
        following_list = []
        async for user in api.following(user_id):
            following_list.append(user.username)

        if not check_following_count(user_login, len(following_list)):

            print("Entered loop to update list")
            # Insert user_login into the database and retrieve its account_id
            account_id = insert_twitter_account(user_login, display_name, len(following_list))

            # Insert every user from the following list into the database
            for username in following_list:
                insert_following(account_id, username)

        print(f"done{x}")

#comment out below lines if you're uploading user for first time
    message = format_following_message()
    send_email("Today's New Followings", message)

if __name__ == "__main__":
    asyncio.run(main())