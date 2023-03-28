"""
Шифрование и расшифрование сообщения с сервиса safenote.co
Create at 27.02.2023 12:43:59
~core/main.py
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

import argparse
import selenium.common.exceptions
from core.cipher import Cipher
from core.privatty import Privatty
from core.clck import LinkShort
import core.errors as errors
from core.settings import LENGTH_PASSWORD
from string import printable


def check(word):
    return all(map(lambda c: c in printable, word))


def main(args: argparse.Namespace):
    if args.action == 'write':
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
        encrypted_massage = Cipher.encrypt_message(args.password,
                                                   args.massage)  # шифруем сообщение через AES -> base64
        try:
            url = Privatty.write_message(str(encrypted_massage)[2:-1])  # записываем зашифрованное сообщение
        except selenium.common.exceptions.TimeoutException:
            raise errors.TimeError("Время запроса превышено!")
        sh_link = LinkShort.short_link(url)  # сокращаем ссылку
        string = sh_link.split('/')[-1]
        hex_arr = ([hex(ord(i)) for i in string])
        return [chr(i) for i in Cipher.vernam(hex_arr, args.password)]
        # далее записываем сокращённую шифрованную URL в файл m4a (нибблы)
    elif args.action == 'read':
        # предварительно вытаскиваем нибблы и получаем шифрованную короткую ссылку
        sh_en_link = args.url
        new_link = []
        for i in range(0, len(sh_en_link) - 1, 2):
            new_link.append(sh_en_link[i] + sh_en_link[i + 1])
        arr_hex = ([hex(int(i, 16)) for i in new_link])
        ex = [hex(i) for i in Cipher.vernam(arr_hex, args.password)]
        sh_link = "https://goo.su/" + Cipher.from_hex_to_text(ex)
        en_massage = Privatty.read_message(sh_link)  # если пароль верен, ссылка отправит на сайт www.privatty.com
        # расшифровываем сообщение в обратном порядке en_massage -> decodebase64 -> decode AES -> massage
        bytes_ex_massage = bytes(en_massage, encoding='utf-8')
        ex_massage = Cipher.decrypt_message(
            args.password,
            bytes_ex_massage
        )
        return str(ex_massage)[2:-1]
