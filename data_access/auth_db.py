from pymongo import MongoClient
from dev_db import get_database
db_name = get_database()
#probably should make these static methods
# when u pass in string you should get the db collection
# not sure if it works if not use db_name['user']
db = {"usr": db_name.user, "account": db_name.accounts}
# not sure if line 8 works if now just pass instring or dot notation
# ie client["users"] or client.users


@staticmethod
def store_keys(userid, privatekey, publickey):
    pass


@staticmethod
def fetch_public_key(username):
    pass


@staticmethod
def fetch_private_key(username):
    pass