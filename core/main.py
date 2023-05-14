"""
Create at 27.02.2023 12:43:59
~core/main.py
"""

import argparse
from core.cipher import Cipher
from core.clck import LinkShort
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
    core.sdarn.onetimesecret.OneTimeSecretSdarn.name: core.sdarn.onetimesecret.OneTimeSecretSdarn
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
        sh_link = LinkShort.short_link(url)  # сокращаем ссылку
        string = sh_link.split('/')[-1]
        hex_arr = ([hex(ord(i)) for i in string])
        if args.debug:
            print(f'URL - {url}\nSHORT URL - {sh_link}\nHEX SHORT URL - {hex_arr}')
        return [chr(i) for i in Cipher.vernam(
            hex_arr,
            args.password
        )]
        # далее записываем сокращённую шифрованную URL в файл m4a (нибблы)
    elif args.ex:
        if args.debug:
            print('------------------------EXTRACT MODE------------------------')
        # предварительно вытаскиваем нибблы и получаем шифрованную короткую ссылку
        sh_en_link = args.url
        new_link = []
        for i in range(0, len(sh_en_link) - 1, 2):
            new_link.append(sh_en_link[i] + sh_en_link[i + 1])
        arr_hex = ([hex(int(i, 16)) for i in new_link])
        ex = [hex(i) for i in Cipher.vernam(
            arr_hex,
            args.password
        )]

        sh_link = "https://goo.su/" + Cipher.from_hex_to_text(ex)
        if args.debug:
            print(f'HEX SHORT URL - {ex}\nSHORT URL - {sh_link}')
        return getSdarnClass(args.name).read(
            sh_link,
            args.password
        )
