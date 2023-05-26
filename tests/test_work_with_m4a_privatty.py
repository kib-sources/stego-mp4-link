"""
Тест на запись/чтение файлов m4a, используя сервис privatty
Create at 27.02.2023 12:43:59
~tests/test_work_with_m4a_privatty.py
EXAMPLES
Перемещаемся в директорию с тестами

>> cd tests

Тест, направленный на проверку нормальной работы с записью/чтением сообщения

>> python3 -m unittest test_work_with_m4a_privatty.TestMain.test1

Тест, направленный на получение ошибки об уже прочитанном ранее сообщении

>> python3 -m unittest test_work_with_m4a_privatty.TestMain.test5

Тест, направленный на ошибку контейнера m4a

>> python3 -m unittest test_work_with_m4a_privatty.TestMain.test6

"""

import argparse
import unittest
import repackage
repackage.up()
from stego import write_read_m4a
import core.errors

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


class TestMain(unittest.TestCase):
    name = 'privatty'
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
        '-l', "--link",
        required=False,
        type=str,
        default='goo',
        choices=['goo'],
        help='enter service')
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

    def test1(self):
        message = 'Hey, Everyone!'
        password = 'password-qwerty'
        pathin = '../poc/sample.m4a'
        pathout = '../poc/stego_massage.m4a'
        args = self.parser.parse_args(["--em", '-p', password, '-m', message, '-i', pathin, '-o', pathout, '-n', self.name])
        write_read_m4a(args)
        args = self.parser.parse_args(["--ex", '-p', password, '-i', pathout, '-n', self.name])
        self.assertEqual(write_read_m4a(args), message)

    def test2(self):
        message = 'Hello, World!'
        password = 'Very-Secret-PASSWORD'
        pathin = '../poc/sample2.m4a'
        pathout = '../poc/stego_massage2.m4a'
        args = self.parser.parse_args(["--em", '-p', password, '-m', message, '-i', pathin, '-o', pathout, '-n', self.name])
        write_read_m4a(args)
        args = self.parser.parse_args(["--ex", '-p', password, '-i', pathout, '-n', self.name])
        self.assertEqual(write_read_m4a(args), message)

    def test3(self):
        message = 'A la ger com a la ger'
        password = 'HappyBirthday'
        pathin = '../poc/sample3.m4a'
        pathout = '../poc/stego_massage3.m4a'
        args = self.parser.parse_args(["--em", '-p', password, '-m', message, '-i', pathin, '-o', pathout, '-n', self.name])
        write_read_m4a(args)
        args = self.parser.parse_args(["--ex", '-p', password, '-i', pathout, '-n', self.name])
        self.assertEqual(write_read_m4a(args), message)

    def test4(self):
        message = 'A la ger com a la ger'
        password = 'HappyBirthday'
        pathin = '../poc/thispathisempty.m4a'
        pathout = '../poc/stego_massage3.m4a'
        args = self.parser.parse_args(["--em", '-p', password, '-m', message, '-i', pathin, '-o', pathout, '-n', self.name])
        with self.assertRaises(core.errors.FileContainerError):
            write_read_m4a(args)

    def test5(self):
        message = 'Message'
        password = 'qwerty123'
        pathin = '../poc/sample4.m4a'
        pathout = '../poc/stego_massage3.m4a'
        args = self.parser.parse_args(["--em", '-p', password, '-m', message, '-i', pathin, '-o', pathout, '-n', self.name])
        write_read_m4a(args)
        args = self.parser.parse_args(["--ex", '-p', password, '-i', pathout, '-n', self.name])
        write_read_m4a(args)
        with self.assertRaises(core.errors.MessageHasAlreadyRead):
            write_read_m4a(args)

    def test6(self):
        message = 'HackTheBox'
        password = 'generating-password'
        pathin = '../poc/sample4.m4a'
        pathout = '../poc/stego_massage3.txt'
        args = self.parser.parse_args(["--em", '-p', password, '-m', message, '-i', pathin, '-o', pathout, '-n', self.name])
        with self.assertRaises(core.errors.FileContainerError):
            write_read_m4a(args)


if __name__ == "__main__":
    unittest.main()