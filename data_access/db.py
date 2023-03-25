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
def updateUserCollection(usr_list, database):
    try:
        was_success = False
        err_txt = 'an error occurred while inserting '
        success_txt = ' insertion was successfully'
        userCollection = database.users
        if len(usr_list) < 1:
            raise ValueError('User list must contain at least one record')
        else:
            # results will have insert id if no insert id it failed
            if len(usr_list) == 1:
                singleResult = userCollection.insert_one(usr_list[0])
                was_success = singleResult is None
                print(err_txt + 'user record') if singleResult is not None else print('account' + success_txt)
            if len(usr_list) > 1:
                multiResult = userCollection.insert_many(usr_list)
                was_success = multiResult is None
                print(err_txt + 'user records') if multiResult is not None else print('users' + success_txt)

    except Exception as err:
        print(err)
        raise
    return was_success


@staticmethod
def updateAccountsCollection(account_list, database):
    try:
        was_success = False
        err_txt = 'an error occurred while inserting '
        success_txt = ' insertion was successfully'
        accountCollection = database.accounts
        if len(account_list) < 1:
            raise ValueError('account list must contain at least one record')
        else:
            if len(account_list) == 1:
                singleResult = accountCollection.insert_one(account_list[0])
                was_success = singleResult is None
                print(err_txt + 'account record') if singleResult is not None else print('account' + success_txt)

            if len(account_list) > 1:
                multiResult = accountCollection.insert_many(account_list)
                was_success = multiResult is None
                print(err_txt + 'account records') if multiResult is not None else print('accounts' + success_txt)

    except Exception as err:
        print(err)
        raise
    return was_success


@staticmethod
def insert_user(user):
    try:
        was_success = False
        success_txt = 'User successfully inserted'
        err_txt = 'A error occurred while inserting user'
        if user is not None:
            collection = db['users']
            singleResult = collection.insert_one(user)
            print(success_txt) if singleResult is not None else print(err_txt)
            was_success = singleResult is None
        else:
            raise ValueError('User object cannot be empty')
    except Exception as err:
        print(err)
    return was_success


@staticmethod
def getUserId(usrname):
    try:
        if usrname is None:
            raise ValueError('Username is required to find user id')
        else:
            usrCollection = db['users']
            usr = usrCollection.find_ome({'username': usrname})
            if usr is None:
                print('No user was found for username: ' + usrname)
            else:
                # dictionary is returned
                usrId = usr['userId']
    except Exception as err:
        print(err)
    return usrId if usrId is not None else ''


@staticmethod
def authenticate_user(username, plain_txt_pwd):
    # get
    pass

@staticmethod
def compare_passwords(username, plain_txt):
        pass
