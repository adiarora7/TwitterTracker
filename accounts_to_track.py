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

accounts_to_track = [("eladgil", "Elad Gil", 6535212),
                     ("thilokonzok", "Thilo Konzok", 72551143),
                     ("eshanshetty01", "Eshan Shetty", 784057265158516736)]


#accounts_to_track = [("tarqbash93", "Tarek Akkad", 1499282838717284352),("adiarora710", "Adi Arora", 1213877414800973825)]
# ("nathanbenaich", "Nathan Benaich", 422388777),

# ("adiarora710", "Adi Arora", 1213877414800973825),

