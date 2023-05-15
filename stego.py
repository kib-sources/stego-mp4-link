"""
Запись и чтение сообщения с сервиса одноразовых записок
Create at 27.02.2023 12:43:59
~stego.py
Examples bash:
~$python3 stego.py --em -p password123 -m massage -i poc/sample2.m4a -o poc/stego.m4a

~$python3 stego.py --ex -p password123 -i poc/stego.m4a
"""

import argparse
from core.main import main
from core.write_read_m4a.write import main_write, main_read
from core.errors import *
from core.settings import API_TOKEN

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

Message = str
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '--em', '--embed',
    action='store_true',
    help='embed your message')
parser.add_argument(
    '--ex', '--extract',
    action='store_true',
    help='extract encrypted message')
parser.add_argument(
    "-p", "--password",
    type=str,
    help='enter your password')
parser.add_argument(
    "-m", "--massage",
    type=str,
    help='enter your massage')
parser.add_argument(
    '-i', "--input",
    type=str,
    help='enter <file_path> to *.m4a file')
parser.add_argument(
    '-o', "--output",
    type=str,
    help='enter <file_path> to *.m4a file')
parser.add_argument(
    '--env',
    action='store_true',
    help="print your env"
)
parser.add_argument(
    '-n', "--name",
    required=False,
    type=str,
    default='privatty',
    choices=['privatty', 'onetimesecret'],
    help='enter service')
parser.add_argument(
    '-l', "--link",
    required=False,
    type=str,
    default='goo',
    choices=['goo'],
    help='enter service')
parser.add_argument(
    '-q', "--quiet",
    action='store_true',
    help='quiet mode')
parser.add_argument(
    '-d', "--debug",
    action='store_true',
    help='debug mode')
parser.add_argument(
    '-v', '--version',
    action='version',
    version='%(prog)s 1.0',
    help="Show program's version number and exit")
parser.add_argument(
    '-?', '-h', '--help',
    action='help',
    default=argparse.SUPPRESS,
    help='Show this help message and exit.')


def print_banner():
    print("""
          █████                                               █████ █████
         ░░███                                               ░░███ ░░███
  █████  ███████    ██████   ███████  ██████  █████████████   ░███  ░███ █  ██████
 ███░░  ░░░███░    ███░░███ ███░░███ ███░░███░░███░░███░░███  ░███████████ ░░░░░███
░░█████   ░███    ░███████ ░███ ░███░███ ░███ ░███ ░███ ░███  ░░░░░░░███░█  ███████
 ░░░░███  ░███ ███░███░░░  ░███ ░███░███ ░███ ░███ ░███ ░███        ░███░  ███░░███
 ██████   ░░█████ ░░██████ ░░███████░░██████  █████░███ █████       █████ ░░████████
░░░░░░     ░░░░░   ░░░░░░   ░░░░░███ ░░░░░░  ░░░░░ ░░░ ░░░░░       ░░░░░   ░░░░░░░░
                            ███ ░███
                           ░░██████
                            ░░░░░░       
""")


def write_read_m4a(args: argparse.Namespace) -> Message:
    if args.env:
        if API_TOKEN is None:
            raise EnvironmentError("Не задана переменная окружения API_TOKEN")
        else:
            print(f'Your API token {API_TOKEN}')
            exit()
    if args.em + args.ex == 0:
        raise FlagsError("Не введён флаг --ex или флаг --em")
    if args.em and args.ex or args.debug and args.quiet:
        raise FlagsError("Введённые флаги несовместимы")
    if args.em:
        link = main(args)
        if not args.output:
            raise FileContainerError("Не введён флаг -o --output")
        if args.output.split('.')[-1] != 'm4a':
            raise FileContainerError("Файл не в формате m4a!")
        main_write(link, args.input, args.output, args.debug)
        if not args.quiet:
            print('\033[31m' + 'Message has been interspersed successfully!' + '\033[0m')
    if args.ex:
        if not args.input:
            raise FlagsError("Не задан флаг -i --input")
        link = main_read(args.input)
        args.url = link
        ex_massage = main(args)
        print("Расшифрованное сообщение:  " + ex_massage + '\033[31m')
        print("Пароль верен!" + '\033[0m')
        return ex_massage


if __name__ == "__main__":
    args = parser.parse_args()
    if not args.quiet and not args.env:
        print_banner()
    write_read_m4a(args)
