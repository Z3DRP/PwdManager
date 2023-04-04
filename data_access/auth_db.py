from pymongo import MongoClient
from data_access.dev_db import get_database
#probably should make these static methods
# when u pass in string you should get the db collection
# not sure if it works if not use db_name['user']
# not sure if line 8 works if now just pass instring or dot notation
# ie client["users"] or client.users


@staticmethod
def store_auth(authInfo):
    try:
        authCollection = get_db()
        result = authCollection.insertOne(authInfo)
        was_success = result is not None
    except Exception as err:
        print(err)
    return was_success


@staticmethod
def update_public_key(usrid, key):
    try:
        authCollection = get_db()
        result = authCollection.update_one(
            {'user_id': usrid},
            {"$set": {'public_key': key}},
            upsert=True
        )
        # not sure if acknowledge is true if upsert fialed
        # was_success = result.acknowledge
        was_success = result.modified_count > 0
    except Exception as err:
        print(err)
    return was_success


@staticmethod
def fetch_public_key(usrid, usrname):
    try:
        authCollection = get_db()
        auth = authCollection.find({
            "$and": [{
                'user_id': {"$eq": usrid}
            },
            {
                'username': {"$eq": usrname}
            }]
        })
        return auth if auth is not None else None
    except Exception as err:
        print(err)


def get_db():
    db = get_database()
    return db.auths
