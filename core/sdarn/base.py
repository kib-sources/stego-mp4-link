"""
Базовый класс для сервисов временных записок
Create at 06.05.2023 21:55:54
~core/sdarn/base.py
"""

from typing import Optional
import requests
import selenium

import core.errors
from core.cipher import Cipher

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

Link = str
Message = str
Key = str
MaxLength = int


class BaseSdarn:
    """
    self-destruct after being read notes.
    """
    name = None
    _base_url = None

    @classmethod
    def check_access(cls) -> bool:
        """
        Проверка что cls._base_url доступен и не заблокирован
        """
        try:
            res = requests.get(cls._base_url, timeout=5)
            if cls._base_url != res.url:
                return False
        except requests.exceptions.ReadTimeout:
            return False
        return True

    @classmethod
    def max_length(cls):
        """
        возвращает максимальную длину возможного записываемого сообщения
        без учёта перевода в base64
        """
        return NotImplemented

    @classmethod
    def raw_write(cls, row_message: Message) -> Link:
        """
        Запись сообщения row_message и получения ссылки
        """
        return NotImplemented

    @classmethod
    def raw_read(cls, link: Link) -> Optional[Message]:
        """
        Прочитать сообщение по ссылке,
        или вернуть None, если его нет
        """
        return NotImplemented

    @classmethod
    def write(cls, message: Message, key: Key) -> Link:
        """
        Шифрование сообщения и вызов функции записи raw_write
        """
        if len(message) + len(message) * 0.34 > cls.max_length():  # base64 увеличивает кол-во символов в 1/3 раза
            raise core.errors.LengthMassage("Количество символов должно быть не больше  " + str(cls.max_length()))
        if not cls.check_access():
            raise core.errors.ServiceError("Ошибка доступа к сервису")
        encrypted_massage = Cipher.encrypt_message(key,
                                                   message)  # шифруем сообщение через AES -> base64
        try:
            url = cls.raw_write(str(encrypted_massage)[2:-1])
            return url
        except selenium.common.exceptions.TimeoutException:
            raise core.errors.TimeError("Время запроса превышено!")

    @classmethod
    def read(cls, link: Link, key: Key) -> Message:
        """
        Вызов функции raw_read, расшифрование сообщения
        """
        encrypted_massage = cls.raw_read(link)
        bytes_ex_massage = bytes(encrypted_massage, encoding='utf-8')
        ex_massage = Cipher.decrypt_message(
            key,
            bytes_ex_massage
        )
        return str(ex_massage)[2:-1]

