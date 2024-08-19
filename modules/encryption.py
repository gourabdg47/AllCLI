import os
import base64
import getpass
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def derive_key_from_password(password: str, salt: bytes) -> bytes:
    """Derives a cryptographic key from the given password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_file(filepath: str):
    try:
        password = getpass.getpass(prompt="Enter encryption password: ")
        salt = os.urandom(16)
        key = derive_key_from_password(password, salt)

        with open(filepath, 'rb') as file:
            data = file.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(filepath, 'wb') as file:
            file.write(salt + encrypted)

        logging.info(f"File '{filepath}' encrypted successfully.")
    except Exception as e:
        logging.error(f"Error encrypting file '{filepath}': {e}")
        raise

def decrypt_file(filepath: str):
    try:
        password = getpass.getpass(prompt="Enter decryption password: ")

        with open(filepath, 'rb') as file:
            salt = file.read(16)
            encrypted_data = file.read()

        key = derive_key_from_password(password, salt)

        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data)

        with open(filepath, 'wb') as file:
            file.write(decrypted)

        logging.info(f"File '{filepath}' decrypted successfully.")
    except Exception as e:
        logging.error(f"Error decrypting file '{filepath}': {e}")
        raise
