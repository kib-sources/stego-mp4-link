"""
...

Create at 12.02.2023 00:00:00
~/poc/poc_m4a_links.py
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

import sys

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
nibble2minutes_ret = {value: key for (key, value) in nibble2minutes.items()}
nibble2seconds_ret = {value: key for (key, value) in nibble2seconds.items()}


def nib(link: str) -> list[str]:
    reference_split = link.split('/')[-1]
    nibbles = [nibble for nibble in reference_split.encode('ascii').hex()]
    return nibbles


def read(filepath: str) -> list:
    m4a_chunks = []
    with open(filepath, 'rb') as f:
        while True:
            chunk_length = f.read(4)
            chunk_length_num = int.from_bytes(chunk_length, "big")
            if len(chunk_length) < 4 and chunk_length_num != 0:
                raise Exception("ERROR: некорректный формат!")
            chunk_length_hex = chunk_length.hex()

            if chunk_length_num == 0:
                break
            chunk_type = f.read(4)
            chunk_type_decode = chunk_type.decode('utf-8')
            chunk_type_hex = chunk_type.hex()

            chunk_data = chunk_length_hex + chunk_type_hex + f.read(chunk_length_num - 8).hex()

            chunks = {
                'Length': chunk_length_num,
                'Type': chunk_type_decode,
                'Data': chunk_data,
            }
            m4a_chunks.append(chunks)
    return m4a_chunks


def toseconds(nibbles: list, index: int) -> str:
    day = nibble2day[nibbles[index]]
    hour = nibble2hour[nibbles[index + 1]]
    minutes = nibble2minutes[nibbles[index + 2]]
    seconds = nibble2seconds[nibbles[index + 3]]
    count = (day - 1) * 86400 + hour * 3600 + minutes * 60 + seconds
    a = hex(count)[2:]
    while len(a) != 8:
        a = '0' + a
    return a


def en(chunks: list, nibbles: list[chr]) -> str:
    index = 0
    moov = {}
    for i in range(len(chunks)):
        if chunks[i]['Type'] == 'moov':
            moov = chunks[i]
            break
    arr = []
    for i in range(len(moov['Data'])):
        if (i < 40 or i > 55) and (i < 272 or i > 279):
            # диапазон (44, 55) - сдвиг относительно начала чанка moov, содержащий create date и modify date
            # диапазон (272, 279) - сдвиг относительно начала чанка moov, содержащий track create date
            arr.append(moov['Data'][i])
        if i == 40:
            # достигли начала create date и modify date
            for j in toseconds(nibbles, index):
                arr.append(str(j))
            index += 4
            for j in toseconds(nibbles, index):
                arr.append(str(j))
            index += 4
        elif i == 272:
            # достигли начала track create date
            for j in toseconds(nibbles, index):
                arr.append(str(j))
    return "".join(arr)


def new_file_str(chunks: list, new_chunk: str) -> str:
    new_str = ''
    for i in range(len(chunks)):
        if chunks[i]['Type'] == 'moov':
            chunks[i]['Data'] = new_chunk
    new_str = chunks[0]['Data'] + chunks[1]['Data'] + chunks[2]['Data'] + chunks[3]['Data']

    return new_str


def write(link: str, input_file: str, pathstego: str) -> None:
    with open(pathstego, 'wb+') as fh:
        m4a_chunks = read(input_file)
        nibbles_from_link = nib(link)
        new_chunks = en(m4a_chunks, nibbles_from_link)
        fh.write(bytes.fromhex(new_file_str(m4a_chunks, new_chunks)))


def ex(chunks: list) -> str:
    moov = {}
    for i in range(len(chunks)):
        if chunks[i]['Type'] == 'moov':
            moov = chunks[i]
            break
    str1 = ''
    str2 = ''
    str3 = ''

    for i in range(len(moov['Data'])):
        if 40 <= i <= 47:
            # диапазон [40, 47] - свдиг относительно начала чанка moov, содержащий create date
            str1 += moov['Data'][i]
        elif 48 <= i <= 55:
            # диапазон [48, 55] - свдиг относительно начала чанка moov, содержащий modify date
            str2 += moov['Data'][i]
        elif 272 <= i <= 279:
            # диапазон [272, 279] - свдиг относительно начала чанка moov, содержащий track create date
            str3 += moov['Data'][i]

    arr = nibble_ret(int(str1, 16)) + nibble_ret(int(str2, 16)) + nibble_ret(int(str3, 16))
    str = ''
    for i in range(len(arr)):
        str += arr[i]

    ans = bytes.fromhex(str).decode('UTF-8')
    return "https://clck.ru/" + ans


def nibble_ret(sec: int) -> list[int]:
    nibble_arr = []
    day = (sec // 86400) + 1
    sec = sec % 86400
    hour = sec // 3600
    sec = sec % 3600
    minutes = sec // 60
    seconds = sec % 60
    nibble_arr.append(nibble2day_ret[day])
    nibble_arr.append(nibble2hour_ret[hour])
    nibble_arr.append(nibble2minutes_ret[minutes])
    nibble_arr.append(nibble2seconds_ret[seconds])
    return nibble_arr


if __name__ == "__main__":
    try:
        param_name = sys.argv[1]
        if param_name == '--em':
            link = sys.argv[2]
            if sys.argv[3] == '--in':
                input_file = sys.argv[4]
            if sys.argv[5] == '--out':
                pathstego = sys.argv[6]
            write(link, input_file, pathstego)
        elif param_name == '--ex':
            input_file = sys.argv[2]
            print(ex(read(input_file)))
    except IndexError:
        raise Exception("ERROR: недостаточно аргументов")

