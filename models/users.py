import rsa

class User:

    def __init__(self, usrname, email, plainTxtPwd):
        self._username = usrname
        self._email = email
        self._plaintxt_password = plainTxtPwd
        self._encryptedPwd = self.encrypt_pwd()
        self.public_key, self._private_key = self.get_keys()

    def get_username(self):
        return self._username

    def get_email(self):
        return self._email

    def get_plain_txt_password(self):
        return self._plaintxt_password

    def get_keys(self):
        try:
            public, private = rsa.newkeys(512)
        except Exception as err:
            print('Error::', err)
        return [public, private]

    def encrypt_pwd(self):
        try:
            # pass in plainTxt as byteString and the public key to encrypt
            self._encryptedPwd = rsa.encrypt(self._plaintxt_password.encode(), self.public_key)
        except Exception as err:
            print("Error:: ", err)

    def decrypt_pwd(self):
        return rsa.decrypt(self._encryptedPwd, self._private_key).decode()

    def compare_pwd(self, entered_pwd):
        return self.decrypt_pwd() == entered_pwd

    # maybe add isValid method to check data is correct types
