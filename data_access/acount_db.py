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
def insert_account(account):
    pass


@staticmethod
def fetch_account(account_name):
    pass


@staticmethod
def update_account(account):
    pass
