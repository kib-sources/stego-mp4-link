"""
Получение сокращённой ссылки с использованием API-токена сервиса goo.su
Create at 27.02.2023 12:43:59
~core/clck.py
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

from core.settings import API_TOKEN
import requests
from requests.exceptions import ConnectionError
import core.errors as errors


class LinkShort:
    url_api = 'https://goo.su/api/links/create'

    @classmethod
    def short_link(cls, url: str) -> str:
        data = {
            "url": url,
        }
        headers = {'x-goo-api-token': API_TOKEN}  # API-токен
        try:
            r = requests.post(cls.url_api,
                              headers=headers,
                              data=data)  # отправляем запрос на сайт с параметрами
            return r.json()['short_url']
        except ConnectionError:
            raise errors.ConnectionError("Соединение прервано!")
