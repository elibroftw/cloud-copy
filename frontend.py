# Make sure one instance
# If not authenticated, first authenticate, provide PC name
# Server returns a token which is saved

import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# TODO: maybe make into a tray application?


def create_key(provided_password: str) -> bytes:
    password = provided_password.encode()  # Convert to type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'',
        iterations=100000,
        backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
    return key
    # with open('.key', 'wb') as f: f.write(key)


def start_service(): pass


def encrypt(key, message: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(message)


def decrypt(key, encrypted: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(encrypted)
# Once autheticated, use the password to make a key
# https://nitratine.net/blog/post/encryption-and-decryption-in-python/
# Then run as a service
# For every copied data, send the token with the data
# Token is unencrypted
# Data is encrypted with the hashed password
# Make sure to handle no wifi
# Socket connection might be required with the server
# No copied notifications / sent notifications
