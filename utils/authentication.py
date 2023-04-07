from data_access import user_db, auth_db
from utils.encryption import *


# checks entered password against stored encrypted_password; returns True if password matches, False otherwise.
@staticmethod
def verify_password(username, entered_password):
    user = None
    try:
        user = user_db.fetch_user(username)
        if user is None:
            raise ValueError('That user does not exist')
        else:
            encrypted_entered_password = encrypt_password(entered_password, user.get_salt())
        if user.get_password() == encrypted_entered_password:
            verified_password = True
        else:
            verified_password = False
        return verified_password
    except Exception as err:
        print(err)
