"""
Шифрование и расшифровка ссылки и сообщения
Create at 27.02.2023 12:43:59
~core/cipher.py
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

KEY_LENGTH = 32
STEGO_ENCODING = 'ascii'


class Cipher:
    # храним соль и nonce как константы
    salt = b'\xf3v\xf4\x9d]\\\x1f\x1dG\xca\xa0)\xd6\xdaDF'
    nonce = b'\xcdw\x18\x95g\xe7d'
    count = 235125

    @classmethod
    def encrypt_message(cls, password: str, massage: str) -> bytes:
        key = PBKDF2(password,
                     cls.salt,
                     KEY_LENGTH,
                     count=cls.count,
                     hmac_hash_module=SHA512)
        data = bytes(massage, encoding=STEGO_ENCODING)
        e_cipher = AES.new(key, AES.MODE_EAX, nonce=cls.nonce)  # шифруем сообщение
        e_data = str(e_cipher.encrypt(data))[2:-1]
        return base64.b64encode(bytes(str(e_data), encoding=STEGO_ENCODING))  # переводим в кодировку base64

    @classmethod
    def decrypt_message(cls, password: str, base64_message: bytes):
        message_bytes = str(b64decode(base64_message))
        s = message_bytes[2:-1].replace('\\\\', '\\')
        result = s.encode('latin1').decode('unicode_escape').encode('latin1')
        key = PBKDF2(password,
                     cls.salt,
                     KEY_LENGTH,
                     count=cls.count,
                     hmac_hash_module=SHA512)

        d_cipher = AES.new(key, AES.MODE_EAX, nonce=cls.nonce)
        d_data = d_cipher.decrypt(result)  # расшифровываем сообщение
        return d_data

    @classmethod
    def from_hex_to_text(cls, hex_arr):
        return ''.join([chr(int(i, 16)) for i in hex_arr])

    @classmethod
    def vernam(cls, hex_arr, password):
        text = [int(i, 16) for i in hex_arr]
        """ Returns the Vernam Cypher for given string and key """
        arr = []  # the Cypher text
        p = 0  # pointer for the key
        for char in text:
            arr.append(char ^ ord(password[p]))
            p += 1
            if p == len(password):
                p = 0
        return arr
