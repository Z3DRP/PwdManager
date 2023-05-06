import rsa
import hashlib
from utils.Secret import get_salt
from data_access import user_db, auth_db
from utils.random_generator import generateId


class User:
    # look at flask friday playlist to look at hashing pwds so
    # public and private keys dont have to be tracked
    def __init__(self, id=None, usrname=None, email=None, pwd=None):
        self.userId = id
        self.username = usrname
        self.email = email
        self.password = pwd

    @classmethod
    def set_new_User(cls, username, email, password):
        userId = generateId()
        encryptedPwd = cls.set_password(password)
        return cls(id=userId, usrname=username, email=email, pwd=encryptedPwd)

    @classmethod
    def set_user_login(cls, username, password):
        try:
            userId = user_db.fetch_user_id(username)
            if not userId.get('userExists'):
                raise Exception(f'User not found')
            else:
                return cls(userId['userId'], usrname=username, email=None, pwd=password)
        except Exception as err:
            raise Exception('Authentication error') from err

    @classmethod
    def set_password(cls, password):
        salt = get_salt()
        password += salt
        return cls.encrypt_sha512(password)

    def verify_password(self, usrname, entered_pwd):
        try:
                usr = user_db.fetch_user(usrname)
                if not usr.get('userExists'):
                    raise ValueError(usr.get('message'))
                else:
                    newHash = self.get_hash(entered_pwd)
                    if newHash == usr['userData']['password'] and self.userId == usr['userData']['userId']:
                        return {
                            'isMatch': True,
                            'userId': usr['userData']['userId'],
                            'password': usr['userData']['password'],
                            'email': usr['userData']['email']
                        }
                    else:
                        return {
                            'isMatch': False,
                            'message': 'Invalid password, check password and try again'
                        }

        except Exception as err:
            raise Exception(err) from err

    def get_hash(self, plainTxt):
        salt = get_salt()
        plainTxt += salt
        return self.encrypt_sha512(plainTxt)

    def encrypt_sha512(self, plaintxt):
        return hashlib.sha512(plaintxt.encode('utf-8')).hexdigest()

    @staticmethod
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

    def decrypt_pwd(self, encrypted_pwd, privatekey):
        return rsa.decrypt(encrypted_pwd, self.private_key).decode()

    # decryption to test if public key will work it should
    def decrypt_pwd_public(self, encrypted_pwd, public_key):
        return rsa.decrypt(encrypted_pwd, public_key).decode()

    def authenticated_user(self, usrname, email, id):
        self.username = usrname
        self.email = email
        self.userid = id

    def get_user_id(self):
        return self.userId

    def set_username(self, usrname):
        self.username = usrname

    def get_username(self):
        return self.username

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def get_password(self):
        return self.encrypted_pwd
    # maybe add isValid method to check data is correct types

    def plain_text_password(self):
        self.encrypted_pwd

    def getUserJson(self):
        return {
            'userId': self.userId,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

    #v1 pwd encryption methods
    # def set_password(self, plaintxt, publicKey=None, privateKey=None):
    #     try:
    #         if publicKey is None and privateKey is None:
    #             public_key, private_key = self.get_keys()
    #         else:
    #             public_key = publicKey
    #             private_key = privateKey
    #         self.password = self.encrypt_pwd(plaintxt, public_key)
    #
    #         if self.password is not None:
    #             was_success = auth_db.store_auth(self.userid, private_key, public_key)
    #             print('auth success:: true')
    #     except Exception as err:
    #         print(err)


    # @staticmethod
    # def verify_password(self, usrname, entered_pwd):
    #     try:
    #         usr = user_db.fetch_user(usrname)
    #         # not sure if this will work test
    #         if not usr.get('userExists'):
    #             raise ValueError('Error username ' + usrname + ' does not exist')
    #         else:
    #             publicKey = self.fetch_public_key(usrname)
    #             if publicKey is None:
    #                 raise ValueError('Unable to authenticate user')
    #         return {
    #             'isMatch': self.encrypt_pwd(entered_pwd, publicKey) == usr['password'],
    #             'userId': usr.userData['userid'],
    #             'email': usr.UserData['email']
    #         }
    #
    #     except Exception as err:
    #         print(err)
