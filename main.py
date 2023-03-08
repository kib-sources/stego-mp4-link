"""
Работа с консолью
Create at 27.02.2023 12:43:59
~main.py
Example:
    $ python3 main.py -a write -p password123 -m 'Very secret massage!!!'
    ...
    $ python3 main.py -a read -p password123 -u https://goo.su/0x80xe0x10x380x3
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
from string import ascii_letters, digits, punctuation

parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--password",
    type=str,
    help='enter your password',
    required=True)
parser.add_argument(
    "-m", "--massage",
    type=str,
    required=False,
    help='enter your massage')
parser.add_argument(
    "-a", "--action",
    required=True,
    choices=['write', 'read'])
parser.add_argument(
    '-u', "--url",
    required=False,
    type=str,
    help='enter URL')


def check(word):
    return all(map(lambda c: c in ascii_letters + digits + punctuation, word))


def main(args: argparse.Namespace) -> str:
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
        print(f'Изначальное URl {url}')
        print(f'Сообщение в privatty - {str(encrypted_massage)[2:-1]}')
        sh_link = LinkShort.short_link(url)  # сокращаем ссылку
        print(f'Сокращённая незашифрованная URL: {sh_link}')
        string = sh_link.split('/')[-1]
        hex_arr = ([hex(ord(i)) for i in string])
        en = [hex(i) for i in Cipher.vernam(hex_arr, args.password)]
        print(f'Сокращённая зашифрованная URL: https://goo.su/{"".join(en)}')
        return 'https://goo.su/' + "".join(en)
        # далее записываем сокращённую шифрованную URL в файл m4a (нибблы)
    elif args.action == 'read':
        # предварительно вытаскиваем нибблы и получаем шифрованную короткую ссылку
        sh_en_link = args.url
        sh_en_link = sh_en_link
        print(f'Полученная ссылка: {sh_en_link}')
        arr = [int(i, 16) for i in sh_en_link.split('/')[-1].split('0x') if i]
        arr_hex = [hex(i) for i in arr]
        ex = [hex(i) for i in Cipher.vernam(arr_hex, args.password)]
        sh_link = "https://goo.su/" + Cipher.from_hex_to_text(ex)
        print(f"Расшифрованная ссылка: {sh_link}")
        en_massage = Privatty.read_message(sh_link)  # если пароль верен, ссылка отправит на сайт www.privatty.com
        # расшифровываем сообщение в обратном порядке en_massage -> decodebase64 -> decode AES -> massage
        print(f'Полученное сообщение: {en_massage}')
        ###
        ex_massage = str(Cipher.decrypt_message(
            args.password,
            bytes(en_massage, encoding='utf-8')))[2:-1]
        print("Расшифрованное сообщение:  " + ex_massage + '\033[31m')
        print("Пароль верен!" + '\033[0m')
        return ex_massage


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
    exit()
