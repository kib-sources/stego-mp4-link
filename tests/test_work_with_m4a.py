"""
Тест на запись чтение файлов m4a
Create at 27.02.2023 12:43:59
~tests/test_work_with_m4a.py
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
from stego import write_read_m4a
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

    def test1(self):
        message = 'Hey, Everyone!'
        password = 'password-qwerty'
        pathin = '../poc/sample.m4a'
        pathout = '../poc/stego_massage.m4a'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', message, '-i', pathin, '-o', pathout])
        write_read_m4a(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-o', pathout])
        self.assertEqual(write_read_m4a(args), message)

    def test2(self):
        message = 'Hello, World!'
        password = 'Very-Secret-PASSWORD'
        pathin = '../poc/sample2.m4a'
        pathout = '../poc/stego_massage2.m4a'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', message, '-i', pathin, '-o', pathout])
        write_read_m4a(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-o', pathout])
        self.assertEqual(write_read_m4a(args), message)

    def test3(self):
        message = 'A la ger com a la ger'
        password = 'HappyBirthday'
        pathin = '../poc/sample3.m4a'
        pathout = '../poc/stego_massage3.m4a'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', message, '-i', pathin, '-o', pathout])
        write_read_m4a(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-o', pathout])
        self.assertEqual(write_read_m4a(args), message)

    def test4(self):
        message = 'A la ger com a la ger'
        password = 'HappyBirthday'
        pathin = '../poc/thispathisempty.m4a'
        pathout = '../poc/stego_massage3.m4a'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', message, '-i', pathin, '-o', pathout])
        with self.assertRaises(core.errors.NoFile):
            write_read_m4a(args)

    def test5(self):
        message = 'Message'
        password = 'qwerty123'
        pathin = '../poc/sample4.m4a'
        pathout = '../poc/stego_massage3.m4a'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', message, '-i', pathin, '-o', pathout])
        write_read_m4a(args)
        args = self.parser.parse_args(["-a", "read", '-p', password, '-o', pathout])
        write_read_m4a(args)
        with self.assertRaises(core.errors.MessageHasAlreadyRead):
            write_read_m4a(args)

    def test6(self):
        message = 'HackTheBox'
        password = 'generating-password'
        pathin = '../poc/sample4.m4a'
        pathout = '../poc/stego_massage3.txt'
        args = self.parser.parse_args(["-a", "write", '-p', password, '-m', message, '-i', pathin, '-o', pathout])
        with self.assertRaises(core.errors.NoM4a):
            write_read_m4a(args)


if __name__ == "__main__":
    unittest.main()