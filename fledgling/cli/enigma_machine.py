# -*- coding: utf8 -*-
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from fledgling.cli.nest_client import IEnigmaMachine


class MockEnigmaMachine(IEnigmaMachine):
    def decrypt(self, cipher_text):
        return cipher_text

    def encrypt(self, plain_text):
        return plain_text


class FernetEnigmaMachine(IEnigmaMachine):
    def __init__(self, password):
        password_bytes = bytes(password, 'utf-8')
        salt = self._derive_salt(password_bytes)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        self.f = Fernet(key)

    def decrypt(self, cipher_text: str) -> str:
        cipher_bytes = base64.b64decode(cipher_text)
        return str(self.f.decrypt(cipher_bytes), 'utf-8')

    def encrypt(self, plain_text: str) -> str:
        plain_bytes = bytes(plain_text, 'utf-8')
        return str(base64.b64encode(self.f.encrypt(plain_bytes)), 'utf-8')

    def _derive_salt(self, password_bytes: bytes) -> bytes:
        length = len(password_bytes)
        if length >= 16:
            return password_bytes[0:16]
        return password_bytes + bytes('\0' * (16 - length), 'utf-8')
