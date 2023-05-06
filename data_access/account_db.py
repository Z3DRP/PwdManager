from pymongo import MongoClient
from data_access.dev_db import get_database
from models.User import User
from models.Account import Account
from messages.Error_Messages import Errors as error
from messages.Success_Messages import Success as success

#probably should make these static methods
# when u pass in string you should get the db collection
# not sure if it works if not use db_name['user']
# not sure if line 8 works if now just pass instring or dot notation
# ie client["users"] or client.users


@staticmethod
def InsertAccountsCollection(account_list, database):
    try:
        was_success = False
        accountCollection = get_db()
        if len(account_list) < 1:
            raise ValueError('account list must contain at least one record')
        else:
            if len(account_list) == 1:
                singleResult = accountCollection.insert_one(account_list[0])
                was_success = singleResult is None
                print(success.db_success('insert', 'account')) if singleResult is not None else print(error.db_error('insert', 'account'))

            if len(account_list) > 1:
                multiResult = accountCollection.insert_many(account_list)
                was_success = multiResult is None
                print(success.db_success('insert_p', 'accounts')) if multiResult is not None else print(error.db_error('insert', 'accounts'))

    except Exception as err:
        print(err)
        raise
    return was_success


#note parameter passed in must be lower case of model name
# if not spelled the same will not have access to class members and methods
@staticmethod
def insert_account(account):
    try:
        accountCollection = get_db()
        result = accountCollection.insert_one(account)
        if not result.acknowledge:
            raise Exception('An error occurred while storing account')
        elif result.inserted_id is not None:
            return {'wasSuccess': True, 'result': result}
    except Exception as err:
        raise Exception(err) from err


@staticmethod
def fetch_user_account(uid, accountName):
    try:
        accountCollection = get_db()
        result = accountCollection.find({
            "$and": [
                {"userId": {"$eq": uid}},
                {'username': {"$eq": accountName}}
            ]
        })
        if result.count() > 0:
            return {'wasSuccess': True, 'result': result}
        else:
            return {'wasSuccess': False, 'message': 'No account found'}
    except Exception as err:
        raise Exception(err) from err


@staticmethod
def fetch_user_accounts(user):
    try:
        accountCollection = get_db()
        usr_accounts = accountCollection.find({
            "$and": [
                {'userId': {"$eq": user['userId']}},
                {'username': {"$eq": user['username']}}]
        })
        if not usr_accounts.retrieved > 0:
            return {'wasSuccess': False, 'message': error.no_accounts(user['username'])}
        else:
            return {'wasSuccess': True, 'result': usr_accounts}
    except Exception as err:
        raise Exception(err) from err


@staticmethod
def update_account(account):
    try:
        accountCollection = get_db()
        result = accountCollection.update_one(
            {"$and": [
                {'user_id': {"$eq": account.user_id}},
                {'account_id': {"$eq": account.account_id}}
            ]},
            {"$set": {
                'name': account.name,
                'email': account.email,
                'password': account.password
            }},
            upsert=True
        )
        if not result.acknowledge:
            raise ValueError('A issue occurred while connecting')
        elif result.modified_count > 0 or result.upsert_count > 0:
            return {'wasSuccess': True, 'message': success.db_success('update', 'user')}
        else:
            return {'wasSuccess': False, 'message': error.db_error('insert', 'user')}
    except Exception as err:
        raise Exception(err) from err


# TODO since nested array fields are accessed with dot notation and name need update for each 'extra field'
@staticmethod
def update_pin(account):
    try:
        accountCollection = get_db()
        result = accountCollection.update_one(
            {"$and": [
                {'user_id': {"eq": account.user_id}},
                {'account_id': {"$eq": account.account_id}}
            ]},
            {"$set": {
                'name': account.name,
                'email': account.email,
                'password': account.password,
                "field.pin": account.fields['pin']
            }},
            upsert=True
        )
        was_success = result.modified_count > 0
        if result.modified_count > 0:
            return {'wasSuccess': True, 'message': success.db_success('update', 'account')}
        else:
            return {'wasSuccess': False, 'message': error.db_error('update', 'account')}
    except Exception as err:
        raise Exception(err) from err


def get_db():
    db = get_database()
    return db.accounts
