import os
from dotenv import load_dotenv
load_dotenv()

USER1 = os.getenv("USER1")
PASS1 = os.getenv("PASS1")
EMAIL1 = os.getenv("EMAIL1")
MAILPASS1 = os.getenv("MAILPASS1")

USER2 = os.getenv("USER2")
PASS2 = os.getenv("PASS2")
EMAIL2 = os.getenv("EMAIL2")
MAILPASS2 = os.getenv("MAILPASS2")

twitter_accounts = [(USER1, PASS1, EMAIL1, MAILPASS1),
                    (USER2, PASS2, EMAIL2, MAILPASS2)]

accounts_to_track = [("eladgil", "Elad Gil", 6535212)]

