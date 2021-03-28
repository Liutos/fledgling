# -*- coding: utf8 -*-
from fledgling.cli.enigma_machine import FernetEnigmaMachine


def test_fernet_enigma_machine():
    """
    测试FernetEnigmaMachine的加密/解密功能。
    """
    enigma_machine = FernetEnigmaMachine(
        password='1234567',
    )
    test_cases = [
        'Hello, world!',
        '你好，世界！',
        'Hello, 世界！',
        '',
    ]
    for plain_text in test_cases:
        cipher_text = enigma_machine.encrypt(plain_text)
        assert isinstance(cipher_text, str)
        decrypted_text = enigma_machine.decrypt(cipher_text)
        assert decrypted_text == plain_text
