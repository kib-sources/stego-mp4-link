"""
Запись и чтение сообщения с сервиса privatty.py
Create at 27.02.2023 12:43:59
~stego.py
Examples bash:
~$python3 stego.py -a write -p password123 -m Massage -i poc/sample3.m4a -o poc/stego.m4a
~$python3 stego.py -a read -p password123 -o poc/stego.m4a
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
from core.main import main
from core.write_read_m4a.write import main_write, main_read
from core.errors import *
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
parser.add_argument(
    '-i', "--pathin",
    required=False,
    type=str,
    help='enter pathin to *.m4a file')
parser.add_argument(
    '-o', "--pathstego",
    required=False,
    type=str,
    help='enter pathout to *.m4a file')


def write_read_m4a(args: argparse.Namespace) -> str:
    if args.action == 'write':
        link = main(args)
        if args.pathstego.split('.')[-1] != 'm4a':
            raise FileContainerError("Файл не в формате m4a!")
        main_write(link, args.pathin, args.pathstego)
    if args.action == 'read':
        link = main_read(args.pathstego)
        args.url = link
        ex_massage = main(args)
        print("Расшифрованное сообщение:  " + ex_massage + '\033[31m')
        print("Пароль верен!" + '\033[0m')
        return ex_massage


if __name__ == "__main__":
    args = parser.parse_args()
    write_read_m4a(args)