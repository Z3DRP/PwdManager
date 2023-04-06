import bcrypt
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# use to encrypt the user's password for storage
def encrypt_password(plain_text_password, salt):
    # hash the password using bcrypt and user's stored salt
    encrypted_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return encrypted_password


# use to generate key that we don't store. It will be used to encrypt/decrypt user's stored account information
def generate_key(encrypted_password, plain_text_password, salt):
    # convert plain_text_password to bytes
    plain_text_byte_password = plain_text_password.encode()
    # define encryption algorithm
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        # set salt to user's stored salt value so we get same key every time
        salt=salt,
        iterations=500000,
    )
    # generate encryption key
    encryption_key = base64.urlsafe_b64encode(kdf.derive(encrypted_password))
    f = Fernet(encryption_key)
    # encrypt the plain_text_password to act as the user's key. This will not be stored, just regenerated each visit.
    key = f.encrypt(plain_text_byte_password)
    return key

# use to encrypt account information we will store
def encrypt_data(key, unencrypted_data, salt):
    # convert unencrypted_data to bytes
    unencrypted_byte_data = unencrypted_data.encode()
    # define encryption algorithm
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        # set salt to stored salt value so we get same key every time
        salt=salt,
        iterations=500000,
    )
    # use the key to generate the encryption_key
    encryption_key = base64.urlsafe_b64encode(kdf.derive(key))
    f = Fernet(encryption_key)
    # use the encryption_key to encrypt the unencrypted_data
    encrypted_data = f.encrypt(unencrypted_byte_data)
    return encrypted_data


# use to decrypt stored account information
def decrypt_data(key, encrypted_data, salt):
    # define encryption algorithm
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        # set salt to stored salt value so we get same key every time
        salt=salt,
        iterations=500000,
    )
    # use the key to generate the encryption_key
    encryption_key = base64.urlsafe_b64encode(kdf.derive(key))
    f = Fernet(encryption_key)
    # decrypt the encrypted_data using the encryption_key
    return f.decrypt(encrypted_data)



# Test
"""
plain_text_password = "plain_text_password"
unencrypted_data = "secret_data"
salt = bcrypt.gensalt()

print("plain_text_password:", plain_text_password)
encrypted_password = encrypt_password(plain_text_password, salt)
print("encrypted_password: ", encrypted_password)
key = generate_key(encrypted_password, plain_text_password, salt)
print("key: ", key)
print("unencrypted_data: ", unencrypted_data)
encrypted_data = encrypt_data(key, unencrypted_data, salt)
print("encrypted_data: ", encrypted_data)
decrypted_data = decrypt_data(key, encrypted_data, salt)
print("decrypted_data: ", decrypted_data)
"""