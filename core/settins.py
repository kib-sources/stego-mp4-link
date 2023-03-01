"""

TODO


Create at 01.03.2023 17:03:31
~/core/settins.py
"""

__author__ = 'nurovAm'
__copyright__ = 'LGPL'
__license__ = ''  # TODO
__credits__ = [
    'nurovAm',
]
__version__ = "20230301"
__status__ = 'Develop'  # "Production"

import os


from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN', None)
if API_TOKEN is None:
    raise EnvironmentError("Не задана переменная окружения API_TOKEN")
