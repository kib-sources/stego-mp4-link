"""
Создание ошибок
Create at 27.02.2023 12:43:59
~core/errors.py
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


class BaseStegoProjectError(Exception):
    """
    Базовая ошибка проектов stego-m4a+
    """
    pass


class LengthPassword(BaseStegoProjectError):
    """
    Ошибка длины пароля (должна быть больше 6)+
    """
    pass


class NotLatinPassword(BaseStegoProjectError):
    """
    Ошибка нахождения символов из кириллицы в пароле+
    """
    pass


class NotPassword(BaseStegoProjectError):
    """
    Ошибка отсутствия пароля+
    """
    pass


class WrongPassword(BaseStegoProjectError):
    """
    Ошибка неправильного пароля при чтении+
    """
    pass


class NotMessage(BaseStegoProjectError):
    """
    Ошибка отсутствия сообщения+
    """
    pass


class TimeError(BaseStegoProjectError):
    """
    Ошибка превышения времени ожидания для selenium
    """
    pass


class MessageHasRead(BaseStegoProjectError):
    """
    Ошибка при прочтении уже прочитанного ранее сообщения+
    """
    pass


class NotLatinMassage(BaseStegoProjectError):
    """
    Ошибка нахождения символов из кириллицы в сообщении+
    """


class ConnectionError(BaseStegoProjectError):
    """
    Ошибка соединения
    """
    pass
