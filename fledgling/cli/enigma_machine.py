# -*- coding: utf8 -*-
from fledgling.cli.nest_client import IEnigmaMachine


class MockEnigmaMachine(IEnigmaMachine):
    def decrypt(self, cipher_text):
        return cipher_text

    def encrypt(self, plain_text):
        return plain_text
