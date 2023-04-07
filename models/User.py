import bcrypt
from utils.random_generator import generate_id
from utils.encryption import *


class User:
    def __init__(self, username=None, email=None):
        self.username = username
        self.email = email
        self.user_id = None
        self.salt = None
        self.encrypted_password = None
        self.key = None


    # set user's salt, should only be called when creating a new user; salt is should be stored for reuse.
    def set_salt(self):
        try:
            self.salt = bcrypt.gensalt()
        except Exception as err:
            print(err)


    def get_salt(self):
        try:
            return self.salt
        except Exception as err:
            print(err)


    # encrypts plain_text_password with user's salt, gets stored in the database.
    def set_password(self, plain_text_password):
        try:
            self.encrypted_password = encrypt_password(self.salt, plain_text_password)
        except Exception as err:
            print(err)


    def get_password(self):
        try:
            return self.encrypted_password
        except Exception as err:
            print(err)


    # generates a user's key; call on user login, we don't store the key in the database.
    def set_key(self, plain_text_password):
        try:
            self.key = generate_key(self.encrypted_password, plain_text_password, self.salt)
        except Exception as err:
            print(err)


    def get_key(self):
        try:
            return self.key
        except Exception as err:
            print(err)


    # generates a user's user_id; call only once when creating a new user, is stored in database.
    def set_user_id(self):
        try:
            self.user_id = generate_id()
        except Exception as err:
            print(err)


    def get_user_id(self):
        try:
            return self.user_id
        except Exception as err:
            print(err)


    def set_username(self, username):
        try:
            self.username = username
        except Exception as err:
            print(err)

    
    def get_username(self):
        try:
            return self.username
        except Exception as err:
            print(err)
    
    
    def set_email(self, email):
        try:
            self.email = email
        except Exception as err:
            print(err)

    
    def get_email(self):
        try:
            return self.email
        except Exception as err:
            print(err)

    
    def get_user_id(self):
        try:
            return self.user_id
        except Exception as err:
            print(err)
