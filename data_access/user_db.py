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
        if len(usr_list) < 1:
            raise ValueError('User list must contain at least one record')
        else:
            userCollection = get_db()
            # results will have insert id if no insert id it failed
            if len(usr_list) == 1:
                singleResult = userCollection.insert_one(usr_list[0])
                if not singleResult.acknowledged:
                    return {'wasSuccess': False, 'message': 'An error occurred while trying to insert new user'}
                elif singleResult.inserted_id is not None:
                    return {'wasSuccess': True, 'message': success.db_success('insert', 'user')}
            if len(usr_list) > 1:
                multiResult = userCollection.insert_many(usr_list)
                if not multiResult.acknowledged:
                    return {'wasSuccess': False, 'message': error.db_error('insert', 'users')}
                elif multiResult.insert_ids is not None:
                    return {'wasSuccess': True, 'message': success.db_success('insert', 'users')}
                else:
                    return {'wasSuccess': False, 'message': error.db_error('insert', 'users')}
    except Exception as err:
        raise Exception(err) from err


@staticmethod
def insert_user(user):
    try:
        if user is not None:
            collection = get_db()
            result = collection.insert_one(user)
            if not result.acknowledged:
                raise Exception('A issue occurred while trying to connect to database')
            elif result.inserted_id is not None:
                return {'wasSuccess': True, 'message': success.db_success('insert', 'user')}
            else:
                return {'wasSuccess': False, 'message': error.db_error('insert', 'user')}
        else:
            raise ValueError('User object cannot be empty')
    except Exception as err:
        raise Exception(err) from err


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
                return {'userExists': False, 'message': 'User not found'}
            else:
                # dictionary is returned
                return {'userExists': True, 'userId': usr['userId']}
    except Exception as err:
        raise Exception('Unknown error') from err


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
        if result.modified_count > 0:
            return {'wasSuccess': True, 'result': result}
        else:
            return {'wasSuccess': False, 'message': error.db_error('update', 'user')}
    except Exception as err:
        raise Exception(err) from err


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
