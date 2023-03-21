"""
Тесты по вписыванию шифрованного сообщения и получение сообщение по шифрованной ссылки
Create at 04.03.2023 22:43:12
~test/write_read_privatty.py
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
import unittest
from core.main import main
import core.errors


class TestMain(unittest.TestCase):
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

    def test1(self):
        massage = 'Hey, Everyone!'
        password = 'password-qwerty'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        url = main(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-u', url])
        self.assertEqual(main(args), massage)

    def test2(self):
        massage = 'This secret massage!'
        password = 'KiriLlOsIn'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        url = main(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-u', url])
        self.assertEqual(main(args), massage)

    def test3(self):
        massage = 'KIB'
        password = '1234567890'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        url = main(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-u', url])
        self.assertEqual(main(args), massage)

    def test4(self):
        massage = 'Si vis pacem, para bellum'
        password = 'KIRILL2004'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        url = main(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-u', url])
        self.assertEqual(main(args), massage)

    def test5(self):
        massage = 'It`s working!!!'
        password = 'VeRy Se$ret M@ss@ge'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        url = main(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-u', url])
        self.assertEqual(main(args), massage)

    def test6(self):
        massage = 'Massage'
        password = ''
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        with self.assertRaises(core.errors.NotPassword):
            main(args)

    def test7(self):
        massage = ''
        password = 'qwerty123'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        with self.assertRaises(core.errors.NotMessage):
            main(args)

    def test8(self):
        massage = 'Massage'
        password = 'qwerty123'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        url = main(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-u', url])
        main(args)
        with self.assertRaises(core.errors.MessageHasAlreadyRead):
            main(args)

    def test9(self):
        massage = 'This secret massage!'
        password = 'KiriLlOsIn'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        url = main(args)
        password = "AmIrNUroV"
        args = self.parser.parse_args(["-a", "read", '-p', password, '-u', url])
        with self.assertRaises(core.errors.WrongPassword):
            main(args)

    def test10(self):
        massage = 'secret'
        password = 'pass'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', massage])
        with self.assertRaises(core.errors.LengthPassword):
            main(args)

    def test11(self):
        message = 'Very secret message'
        password = 'pass⇐ℵ∞12345'  # non-ASCII symbols
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', message])
        with self.assertRaises(core.errors.NotAsciiPassword):
            main(args)


if __name__ == "__main__":
    unittest.main()
