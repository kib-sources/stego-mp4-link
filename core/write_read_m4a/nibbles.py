"""
Словари для нибблов
Create at 27.02.2023 12:43:59
~write_read_m4a/nibbles.py
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
nibble2day = {
    '0': 1,
    '1': 3,
    '2': 5,
    '3': 7,
    '4': 9,
    '5': 11,
    '6': 13,
    '7': 15,
    '8': 17,
    '9': 19,
    'a': 21,
    'b': 23,
    'c': 25,
    'd': 26,
    'e': 27,
    'f': 28
}
nibble2hour = {
    '0': 1,
    '1': 3,
    '2': 5,
    '3': 7,
    '4': 9,
    '5': 11,
    '6': 13,
    '7': 15,
    '8': 16,
    '9': 17,
    'a': 18,
    'b': 19,
    'c': 20,
    'd': 21,
    'e': 22,
    'f': 23
}
nibble2minutes = {
    '0': 1,
    '1': 5,
    '2': 9,
    '3': 13,
    '4': 17,
    '5': 21,
    '6': 25,
    '7': 29,
    '8': 33,
    '9': 37,
    'a': 41,
    'b': 45,
    'c': 49,
    'd': 54,
    'e': 58,
    'f': 59
}
nibble2seconds = {
    '0': 1,
    '1': 5,
    '2': 9,
    '3': 13,
    '4': 17,
    '5': 21,
    '6': 25,
    '7': 29,
    '8': 33,
    '9': 37,
    'a': 41,
    'b': 45,
    'c': 49,
    'd': 54,
    'e': 58,
    'f': 59
}

nibble2day_ret = {value: key for (key, value) in nibble2day.items()}
nibble2hour_ret = {value: key for (key, value) in nibble2hour.items()}
nibble2minutes_ret: dict = {value: key for (key, value) in nibble2minutes.items()}
nibble2seconds_ret = {value: key for (key, value) in nibble2seconds.items()}
