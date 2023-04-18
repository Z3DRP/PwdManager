from random import seed
from random import randint
from utils.random_generator import generateId


class Account:
    def __init__(self, name, userId, username, email, password):
        self.account_id = self.get_account_id()
        self.user_id = userId
        self.username = username
        self.name = name
        self.email = email
        # TODO if password not None encrypt with util auth
        self.password = password
        # TODO add self.extra_field stores ['fieldName', 'value']
        self.fields = {}

    def get_userid(self):
        return self.user_id

    def get_account_name(self):
        return self.name

    def get_account_email(self):
        return self.email

    def get_account_password(self):
        return self.password

    def get_account_id(self):
        return self.account_id

    def get_field(self, field_name):
        return self.extra_field[field_name]

    def set_name(self, name):
        self.name = name

    def set_email(self, email):
        self.email = email

    def set_password(self, pwd):
        # TODO use auth util to encrypt and decrypt passwords for accounts
        self.password = pwd

    def set_field(self, field_name, field_value):
        self.extra_field[field_name] = field_value

    def get_id(self):
        return generateId()

    # class methods to simulate constructor overloading
    @classmethod
    def createDefaultAccount(cls, usrId):
        accountId = generateId()
        return cls(accountId, usrId, None, None, None)

    def encrypt_password(self):
        pass

    def decrypt_password(self):
        pass

