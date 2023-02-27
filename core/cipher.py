"""
Шифрование и дешифровка ссылки и сообщения
Create at 27.02.2023 12:43:59
~cipher.py
"""

__authors__ = [
    'yourProgrammist',
    'nurovAm'
]
__copyright__ = 'KIB, 2023'
__license__ = 'LGPL'
__credits__ = [
    'yourProgrammist',
    'nurovAm'
]
__version__ = "20230212"
__status__ = "Production"

from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA512
import base64
from base64 import b64decode


# password - english
# massage - english

class Cipher:
    # храним соль и nonce как константы
    salt = b'\xf3v\xf4\x9d]\\\x1f\x1dG\xca\xa0)\xd6\xdaDF'
    nonce = b'\xcdw\x18\x95g\xe7d'

    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123546789"

    @classmethod
    def encryptmassage(self, password: str, massage: str) -> bytes:
        keys = PBKDF2(password, self.salt, 64, count=1000000, hmac_hash_module=SHA512)
        key1 = keys[:32]  # из пароля получаем key
        data = bytes(massage, encoding='utf-8')
        e_cipher = AES.new(key1, AES.MODE_EAX, nonce=self.nonce)  # шифруем сообщение
        e_data = str(e_cipher.encrypt(data))[2:-1]
        return base64.b64encode(bytes(str(e_data), encoding='utf-8'))  # переводим в кодировку base64

    @classmethod
    def decryptmassage(self, password: str, base64_message: bytes):
        message_bytes = str(b64decode(base64_message))
        s = message_bytes[2:-1].replace('\\\\', '\\')
        result = s.encode('latin1').decode('unicode_escape').encode('latin1')
        keys = PBKDF2(password, self.salt, 64, count=1000000, hmac_hash_module=SHA512)
        key1 = keys[:32]

        d_cipher = AES.new(key1, AES.MODE_EAX, nonce=self.nonce)
        d_data = d_cipher.decrypt(result)  # дешифровываем сообщение
        return d_data

    @classmethod
    def encyptlink(self, password: str, shorted_link: str) -> str:
        reference_split = shorted_link.split('/')[-1]
        letter_to_index = dict(zip(self.alphabet, range(len(self.alphabet))))
        index_to_letter = dict(zip(range(len(self.alphabet)), self.alphabet))
        encrypted = ""
        split_message = [
            reference_split[i: i + len(password)] for i in range(0, len(reference_split), len(password))
        ]
        # шифруем через шифр Виженера
        for each_split in split_message:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] + letter_to_index[password[i]]) % len(self.alphabet)
                encrypted += index_to_letter[number]
                i += 1

        return encrypted

    @classmethod
    def decryptlink(self, password: str, enciphered: str) -> str:
        letter_to_index = dict(zip(self.alphabet, range(len(self.alphabet))))
        index_to_letter = dict(zip(range(len(self.alphabet)), self.alphabet))
        decrypted = ""
        split_encrypted = [
            enciphered[i: i + len(password)] for i in range(0, len(enciphered), len(password))
        ]
        # дешифруем
        for each_split in split_encrypted:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] - letter_to_index[password[i]]) % len(self.alphabet)
                decrypted += index_to_letter[number]
                i += 1
        return decrypted
