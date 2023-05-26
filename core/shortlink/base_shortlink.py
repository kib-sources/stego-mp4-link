"""
Базовый класс для сервисов, которые сокращают ссылки
Create at 06.05.2023 21:55:54
~core/shortlink/base_shortlink.py
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

import requests
from core.cipher import Cipher
Link = str
Password = str


class BaseShortLink:
    """
    Базовый класс для сокращения ссылок
    """
    name = None
    _base_url = None

    @classmethod
    def check_access(cls, _base_url: Link) -> bool:
        """
        Проверка доступности сервиса
        """
        try:
            res = requests.get(_base_url, timeout=5)
            if (200 <= res.status_code <= 299) == 0:
                return False
        except requests.exceptions.ReadTimeout:
            return False
        return True

    @classmethod
    def raw_write(cls, sh_link: Link, password: Password) -> list:
        """
        Шифрование ссылки
        """
        string = sh_link.split('/')[-1]
        hex_arr = ([hex(ord(i)) for i in string])
        return [chr(i) for i in Cipher.vernam(
            hex_arr,
            password
        )]

    @classmethod
    def write(cls, url: Link) -> Link:
        """
        Сокращение ссылки, шифрование
        """
        return NotImplemented

    @classmethod
    def raw_read(cls, password: Password, sh_en_link: Link) -> Link:
        """
        Расшифроваине ссылки
        """
        new_link = []
        for i in range(0, len(sh_en_link) - 1, 2):
            new_link.append(sh_en_link[i] + sh_en_link[i + 1])
        arr_hex = ([hex(int(i, 16)) for i in new_link])
        ex = [hex(i) for i in Cipher.vernam(
            arr_hex,
            password
        )]
        return Cipher.from_hex_to_text(ex)

    @classmethod
    def read(cls, password: Password, sh_en_link: Link):
        """
        Получение полноценной ссылки
        """
        return NotImplemented



