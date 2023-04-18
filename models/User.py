import rsa
from data_access import user_db, auth_db
from utils.random_generator import generateId


class User:
    # look at flask friday playlist to look at hashing pwds so
    # public and private keys dont have to be tracked
    def __init__(self, isNewUsr, usrname=None, email=None, pwd=None):
        self.username = usrname
        self.email = email
        self.password = None
        #v1 pwd
        if isNewUsr:
            self.userid = generateId()
            self.public_key, self.private_key = self.get_keys()
            self.set_password(pwd, self.public_key, self.private_key)

        if not isNewUsr:
            try:
                self.userId = user_db.fetch_user_id(usrname)
                self.public_key = None
                self.private_key = None
                self.password = pwd
            except Exception as err:
                print(err)


    #v1 pwd encryption methods
    def set_password(self, plaintxt, publicKey=None, privateKey=None):
        try:
            if publicKey is None and privateKey is None:
                public_key, private_key = self.get_keys()
            else:
                public_key = publicKey
                private_key = privateKey
            self.password = self.encrypt_pwd(plaintxt, public_key)

            if self.password is not None:
                was_success = auth_db.store_keys(self.userid, private_key, public_key)
                print('auth success:: true')
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
        return rsa.decrypt(encrypted_pwd, self.private_key).decode()

    # decryption to test if public key will work it should
    def decrypt_pwd_public(self, encrypted_pwd, public_key):
        return rsa.decrypt(encrypted_pwd, public_key).decode()

    @staticmethod
    def verify_password(self, usrname, entered_pwd):
        try:
            usr = user_db.fetch_user(usrname)
            # not sure if this will work test
            if not usr.get('userExists'):
                raise ValueError('Error username ' + usrname + ' does not exist')
            else:
                publicKey = self.fetch_public_key(usrname)
                if publicKey is None:
                    raise ValueError('Unable to authenticate user')
            return {
                'isMatch': self.encrypt_pwd(entered_pwd, publicKey) == usr['password'],
                'userId': usr.userData['userid'],
                'email': usr.UserData['email']
            }

        except Exception as err:
            print(err)

    def authenticated_user(self, usrname, email, id):
        self.username = usrname
        self.email = email
        self.userid = id
        self.public_key = None
        self.private_key = None
        self.password = None

    def get_user_id(self):
        return self.userid

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


