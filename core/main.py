"""
Create at 27.02.2023 12:43:59
~core/main.py
"""

import argparse
from core.shortlink.goo import Goo
import core.errors as errors
from core.settings import LENGTH_PASSWORD
from string import printable
import core.sdarn.privatty
import core.sdarn.onetimesecret

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


name2sdarn = {
    core.sdarn.privatty.PrivattySdarn.name: core.sdarn.privatty.PrivattySdarn,
    core.sdarn.onetimesecret.OneTimeSecretSdarn.name: core.sdarn.onetimesecret.OneTimeSecretSdarn,
    core.shortlink.goo.Goo.name: core.shortlink.goo.Goo
}


def getSdarnClass(name: str):
    """
    Получаем класс на основе name
    """
    global name2sdarn
    value = name2sdarn.get(name, None)
    if value is None:
        raise errors.NoService("Сервис отсутствует в числе возможных")
    return value


def check(word: str) -> bool:
    """
    Проверка на ASCII
    """
    return all(map(lambda c: c in printable, word))


def main(args: argparse.Namespace):
    if args.em:
        if args.debug:
            print('------------------------EMBED MODE------------------------')
        if not args.password:
            raise errors.NotPassword("Пароль отсутствует!")
        if not args.massage:
            raise errors.NotMessage("Сообщение отсутствует!")
        if len(args.password) < LENGTH_PASSWORD:
            raise errors.LengthPassword("Длина пароля слишком мала")
        if not check(args.password):
            raise errors.NotAsciiPassword("Пароль должен содержать символы только из ASCII")
        if not check(args.password):
            raise errors.NotAsciiMassage("Сообщение должно содержать символы только из ASCII")
        url = getSdarnClass(args.name).write(
            args.massage,
            args.password
        )
        sh_link = getSdarnClass(args.link).write(
            url
        )
        return Goo.raw_write(sh_link, args.password)
    elif args.ex:
        if args.debug:
            print('------------------------EXTRACT MODE------------------------')
        sh_en_link = args.url
        sh_link = getSdarnClass(args.link).read(
            args.password,
            sh_en_link
        )
        if args.debug:
            print(f'SHORT URL - {sh_link}')
        return getSdarnClass(args.name).read(
            sh_link,
            args.password
        )
