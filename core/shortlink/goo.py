"""
Получение сокращённой ссылки с использованием API-токена сервиса goo.su
Create at 27.02.2023 12:43:59
~core/shortlink/goo.py
"""

from core.settings import API_TOKEN
import requests
from requests.exceptions import ConnectionError
import core.errors as errors
from core.shortlink.base_shortlink import BaseShortLink

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
Password = str


class Goo(BaseShortLink):
    """
    Сокращение ссылок, используя сервис goo.su
    """
    name = 'goo'
    _base_url = 'https://goo.su/api/links/create'

    @classmethod
    def write(cls, url: Link) -> Link:
        """
        Отправка POST-запроса на goo.su, получение сокращённой ссылки
        """
        if cls.check_access(cls._base_url):
            raise errors.ConnectionError(f"Сервис {cls.name} не доступен")
        data = {
            "url": url,
        }
        headers = {'x-goo-api-token': API_TOKEN}  # API-токен
        try:
            r = requests.post(cls._base_url,
                              headers=headers,
                              data=data)  # отправляем запрос на сайт с параметрами
            return r.json()['short_url']
        except ConnectionError:
            raise errors.ConnectionError("Соединение прервано!")

    @classmethod
    def read(cls, password: Password, sh_en_link: Link):
        return "https://goo.su/" + cls.raw_read(password, sh_en_link)

