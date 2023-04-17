from pymongo import MongoClient
from data_access.dev_db import get_database
from messages.Success_Messages import Success as success
from messages.Error_Messages import Errors as error
#probably should make these static methods
# when u pass in string you should get the db collection
# not sure if it works if not use db_name['user']
# not sure if line 8 works if now just pass instring or dot notation
# ie client["users"] or client.users

@staticmethod
def InserteUserCollection(usr_list, database):
    try:
        was_success = False
        userCollection = get_db()
        if len(usr_list) < 1:
            raise ValueError('User list must contain at least one record')
        else:
            # results will have insert id if no insert id it failed
            if len(usr_list) == 1:
                singleResult = userCollection.insert_one(usr_list[0])
                was_success = singleResult is None
                print(success.db_success('insert', 'user')) if singleResult is not None else print(error.db_error('insert', 'user'))
            if len(usr_list) > 1:
                multiResult = userCollection.insert_many(usr_list)
                was_success = multiResult is None
                print(success.db_success('insert_p', 'users')) if multiResult is not None else print(error.db_error('insert', 'users'))

    except Exception as err:
        print(err)
        raise
    return was_success


@staticmethod
def insert_user(user):
    try:
        if user is not None:
            collection = get_db()
            result = collection.insert_one(user)
            if not result.acknowledged:
                raise Exception('A issue occurred while trying to connect')
            elif result.insert_count > 0:
                return {'wasSuccess': True, 'message': success.db_success('insert', 'user')}
            else:
                return {'wasSuccess': False, 'message': error.db_error('insert', 'user')}
        else:
            raise ValueError('User object cannot be empty')
    except Exception as err:
        print(err)


@staticmethod
def fetch_user(usrname):
    try:
        if usrname is None:
            raise ValueError('Username is required')
        else:
            usrCollection = get_db()
            usr = usrCollection.find_one({'username': usrname})
            if usr is None:
                return {'userExists': False, 'message': error.no_results('user')}
            else:
                # not sure if this will work
                return {'userExists': True, 'userData': usr}
    except Exception as err:
        raise Exception(err)


@staticmethod
def fetch_user_id(usrname):
    try:
        if usrname is None:
            raise ValueError('Username is required to find user id')
        else:
            usrCollection = get_db()
            usr = usrCollection.find_one({'username': usrname})
            if usr is None:
                print('No user was found for username: ' + usrname)
            else:
                # dictionary is returned
                usrId = usr['userId']
    except Exception as err:
        print(err)
    return usrId if usrId is not None else ''


@staticmethod
def update_user(user):
    try:
        userCollection = get_db()
        result = userCollection.update_one(
            {'user_id': user.usrid},
            {"$set": {
                'username': user.username,
                'email': user.email,
                'password': user.pwd
            }},
            upsert=True
        )
        was_success = result.modified_count > 0
        print(success.db_success('update', 'user')) if was_success else print(error.db_error('update', 'user'))
    except Exception as err:
        print(err)

    return was_success


@staticmethod
def update_many_users(user_list):
    pass


@staticmethod
def authenticate_user(username, usrid):
    pass

@staticmethod
def compare_passwords(username, plain_txt):
    pass


def get_db():
    db = get_database()
    return db.users
