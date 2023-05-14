"""
Базовый класс для сервисов временных записок
Create at 06.05.2023 21:55:54
~core/sdarn/base.py
"""
from typing import Optional
import requests

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
    # базовый урл.
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
        Вызов функции записи raw_write
        """
        row_message = 'TODO'
        return cls.raw_write(row_message)

    @classmethod
    def read(cls, link: Link, key: Key) -> Message:
        assert isinstance(cls._base_url, str)
        assert link.startswith(cls._base_url)
        return cls.raw_read(link)

