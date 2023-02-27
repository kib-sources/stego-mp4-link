"""
Работа с консолью
Create at 27.02.2023 12:43:59
~test.py
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

from selenium.common.exceptions import NoSuchElementException

from cipher import Cipher
from privatty import Privatty
from clck import LinkShort


class PasswordError(Exception):
    pass


class MessageError(Exception):
    pass


if __name__ == "__main__":
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
    args = parser.parse_args()
    # запись
    if args.action == 'write':
        if (set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя').isdisjoint(args.password.lower())) == 0:
            raise PasswordError("Пароль не должен содержать кириллицу")
        if (set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя').isdisjoint(args.massage.lower())) == 0:
            raise PasswordError("Сообщение не должно содержать кириллицу")
        encypted_massage = Cipher.encryptmassage(args.password,
                                                 args.massage)  # шифруем сообщение через AES -> base64
        url = Privatty.write_message(str(encypted_massage)[2:-1])  # записываем зашифрованное сообщение
        print(f'Изначальное URl {url}')
        print(f'Сообщение в privatty - {str(encypted_massage)[2:-1]}')
        sh_link = LinkShort.short_link(url)  # сокращаем ссылку
        print(f'Сокращённая незашифрованная URL: {sh_link}')
        sh_en_link = Cipher.encyptlink(args.password, sh_link)  # шифруем пароль через шифр Виженера
        print(f'Сокращённая зашифрованная URL: https://goo.su/{sh_en_link}')
        # далее записываем сокращённую шифрованную URL в файл m4a (нибблы)
    elif args.action == 'read':
        # предварительно вытаскиваем нибблы и получаем шифрованную короткую ссылку
        sh_en_link = args.url
        print(f'Полученная ссылка: {sh_en_link}')
        sh_link = 'https://goo.su/' + Cipher.decryptlink(args.password,
                                                         sh_en_link.split('/')[-1])  # расшифровываем ссылку
        print(f'Расшифрованная ссылка: {sh_link}')
        try:
            en_massage = Privatty.read_message(sh_link)  # если пароль верен, ссылка отправит на сайт www.privatty.com
        except NoSuchElementException:
            raise PasswordError("Пароль неверный")
        # расшифровавыем сообщение в обратном порядке en_massage -> decodebase64 -> decode AES -> massage
        print(f'Полученное сообщение: {en_massage}')
        ex_massage = str(Cipher.decryptmassage(args.password, bytes(en_massage, encoding='utf-8')))[2:-1]
        if not ex_massage:
            raise MessageError("Сообщение уже было прочитано ранее!")
        print("Расшифрованное сообщение:  " + ex_massage + '\033[31m')
        print("Пароль верен!")

'''
Examples bash
~$ python3 test.py -a write -p password123 -m Hello,World!
Output:
...
...
<short_url>

~$ python3 test.py -a read -p password123 -u short_url
Output:
...
...
Hello,World!
'''
