"""
Получение сокращённой ссылки с использованием API-токена сервиса goo.su
Create at 27.02.2023 12:43:59
~clck.py
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

from requests.exceptions import Timeout, ConnectionError


class LinkShort:
    url_api = 'https://goo.su/api/links/create'

    @classmethod
    def short_link(self, url: str) -> str:
        data = {
            "url": url,
            "is_public": 1,
            "group_id": 2
        }
        headers = {'x-goo-api-token': 'wiA1hUZnkvk7AvotYafUjjpXOsoiIpkj8kGLL8E7UHaLljVnp8nku47wSRvS'}  # API-токен
        try:
            r = requests.post(self.url_api, headers=headers, data=data)  # отправляем запрос на сайт с параметрами
            return r.json()['short_url']
        except Timeout:
            print('Ошибка таймаута')
        except ConnectionError:
            print("Ошибка соединения")
