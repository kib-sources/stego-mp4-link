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
    Базовая ошибка проекта stego-m4a
    """
    pass


class PasswordError(BaseStegoProjectError):
    """
    Базовая ошибка пароля
    """


class MessageError(BaseStegoProjectError):
    """
    Базовая ошибка сообщения
    """


class LengthPassword(PasswordError):
    """
    Ошибка длины пароля
    """
    pass


class NotAsciiPassword(PasswordError):
    """
    Ошибка нахождения символов не из ASCII в пароле
    """
    pass


class NotPassword(PasswordError):
    """
    Пароль отсутствует
    """
    pass


class WrongPassword(PasswordError):
    """
    Ошибка неправильного пароля при чтении
    """
    pass


class NotMessage(MessageError):
    """
    Сообщения отсутствует
    """
    pass


class TimeError(BaseStegoProjectError):
    """
    Ошибка превышения времени ожидания для selenium
    """
    pass


class MessageHasAlreadyRead(MessageError):
    """
    Ошибка при прочтении уже прочитанного ранее сообщения
    """
    pass


class NotAsciiMassage(MessageError):
    """
    Ошибка нахождения символов не из ASCII в сообщении
    """
    pass


class LengthMassage(MessageError):
    """
    Ошибка превышения количества символов для элемента сервиса
    """


class ConnectionError(BaseStegoProjectError):
    """
    Ошибка соединения
    """
    pass


class FileContainerError(BaseStegoProjectError):
    """
    Ошибка *.m4a файла
    """
    pass


class ServiceError(BaseStegoProjectError):
    """
    Ошибка доступа к сервису одноразовых записок
    """
    pass


class NoService(ServiceError):
    """
    Ошибка отсутствия сервиса в числе возможных
    """
    pass


class FlagsError(BaseStegoProjectError):
    """
    Ошибка несовместимости классов
    """
    pass