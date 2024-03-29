"""
Обработка API-токена
Create at 01.03.2023 17:03:31
~/core/settings.py
"""

import os
from dotenv import load_dotenv

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

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN', None)
LENGTH_PASSWORD = 9
if API_TOKEN is None:
    raise EnvironmentError("Не задана переменная окружения API_TOKEN")
