import rsa
from random import randint, seed
from werkzeug.security import generate_password_hash, check_password_hash
from data_access import user_db, auth_db


class User:
    # look at flask friday playlist to look at hashing pwds so
    # public and private keys dont have to be tracked
    def __init__(self, usrname=None, email=None):
        self._usrid = self.generate_id()
        self._username = usrname
        self._email = email
        #v1 pwd
        self._encrypted_pwd = None
        # self.public_key, self._private_key = self.get_keys()

        # v2 of password encryption
        # self._pwd_hash = None

    #v1 pwd encryption methods
    def set_password(self, plaintxt):
        try:
            was_success = None
            public_key, private_key = self.get_keys()
            self._encrypted_pwd = self.encrypt_pwd(plaintxt, public_key)
            if self._encrypted_pwd is not None:
                was_success = auth_db.store_keys(self._usrid, private_key, public_key)
                print('success:: ' + was_success)
        except Exception as err:
            print(err)

    def get_keys(self):
        try:
            public, private = rsa.newkeys(512)
        except Exception as err:
            print('Error::', err)
        return [public, private]

    @staticmethod
    def fetch_public_key(self, usrname):
        publickey = None
        try:
            publickey = auth_db.fetch_public_key(usrname)
        except Exception as err:
            print(err)
        return publickey if publickey is not None else ''

    @staticmethod
    def fetch_private_key(self, usrname):
        privatekey = None
        try:
            privatekey = auth_db.fetch_private_key(usrname)
        except Exception as err:
            print(err)
        return privatekey if privatekey is not None else ''

    # v1 pwd encryption methods
    def encrypt_pwd(self, plaintxt, publickey):
        return rsa.encrypt(plaintxt.encode(), publickey)

    def decrypt_pwd(self, encrypted_pwd, privatekey):
        return rsa.decrypt(encrypted_pwd, self._private_key).decode()

    # decryption to test if public key will work it should
    def decrypt_pwd_public(self, encrypted_pwd, public_key):
        return rsa.decrypt(encrypted_pwd, public_key).decode()

    @staticmethod
    def verify_password(self, usrname, entered_pwd):
        usr = None
        privatekey = None
        try:
            usr = user_db.fetch_user(usrname)
            if usr is None:
                raise ValueError('That user does not exist')
            else:
                privatekey = self.fetch_private_key(usrname)
                if privatekey is None:
                    raise ValueError('Unable to authenticate user')
        except Exception as err:
            print(err)
        return self.decrypt_pwd(usr["_username"], privatekey) == entered_pwd


    #v2 pwd encryption
    # def hash_password(self, plaintxt):
    #     return generate_password_hash(plaintxt)
    #
    # def set_password(self, plaintxt, should_encrypt):
    #     if should_encrypt:
    #         self._pwd_hash = self.hash_password(plaintxt)
    #     else:
    #         self._pwd_hash = plaintxt
    #
    # def get_password_hash(self):
    #     return self._pwd_hash
    #
    # def verify_password(self,  usrname, plaintxt):
    #     try:
    #         usr = user_db.fetch_user(usrname)
    #         if usr is None:
    #             raise Exception('That username does not exist')
    #     except Exception as err:
    #         print(err)
    #     return check_password_hash(usr['_pwd_hash'], plaintxt)

    #end v2 pwd encryption
    def set_username(self, usrname):
        self._username = usrname

    def get_username(self):
        return self._username

    def set_email(self, email):
        self._email = email

    def get_email(self):
        return self._email

    def generate_id(self):
        seed(1)
        generatedId = ''
        # generate id in 00000xxx format
        for number in range(5):
            generatedId += randint(1, 26)
        for letter in range(3):
            generatedId += chr(randint(0, 9))
        return generatedId

    # maybe add isValid method to check data is correct types
