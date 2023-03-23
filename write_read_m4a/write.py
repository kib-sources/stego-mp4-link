"""
Написать запись в файл
На вход от 4 - 7 символов
На выход ссылка
Create at 13.03.2023 18:42:40
~write_read_m4a/write.py
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

from write_read_m4a.nibbles import *
from core.errors import *


def nib(link: list[chr]) -> list[str]:
    reference_split = [str(len(link))] + link
    reference_split = ''.join(reference_split)
    nibbles = [nibble for nibble in reference_split.encode('ascii').hex()]
    return nibbles


def read(filepath: str) -> list:
    m4a_chunks = []
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk_length = f.read(4)
                chunk_length_num = int.from_bytes(chunk_length, "big")
                if len(chunk_length) < 4 and chunk_length_num != 0:
                    raise FormatError("Неверный формат!")
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
    except FileNotFoundError:
        raise NoFile("Файл для вкрапления *.m4a отсутсвует!")


def toseconds(nibbles: list, index: int) -> str:
    day = 0
    hour = 0
    minutes = 0
    seconds = 0
    # Проверяем на наличие остатка в нибблах. В случае если при последнем переводе остается 1 ниббл, переводим только дни, если 2 - переводим дни и часы, и тд...
    if len(nibbles) - index >= 1:
        day = nibble2day[nibbles[index]]
    if len(nibbles) - index >= 2:
        hour = nibble2hour[nibbles[index + 1]]
    if len(nibbles) - index >= 3:
        minutes = nibble2minutes[nibbles[index + 2]]
    if len(nibbles) - index >= 4:
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
    i = 0
    while i < len(moov['Data']):
        if i == 40 and len(nibbles) > 0:
            # достигли начала create date и modify date
            for j in toseconds(nibbles, index):
                arr.append(str(j))
                i+=1
            index += 4
        elif i == 48 and len(nibbles) > 4:
            for j in toseconds(nibbles, index):
                arr.append(str(j))
                i+=1
            index += 4
        elif i == 272 and len(nibbles) > 8:
            # достигли начала track create date
            for j in toseconds(nibbles, index):
                arr.append(str(j))
                i+=1
            index += 4
        elif i == 280 and len(nibbles) > 12:
            # достигли начала track modification time
            for j in toseconds(nibbles, index):
                arr.append(str(j))
                i+=1
        else:
            arr.append(moov['Data'][i])
            i+=1
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


def ex(chunks: list):
    moov = {}
    for i in range(len(chunks)):
        if chunks[i]['Type'] == 'moov':
            moov = chunks[i]
            break
    str1 = ''
    str2 = ''
    str3 = ''
    str4 = ''
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
        elif 279 <= i <= 287:
            # диапазон [279, 287] - свдиг относительно начала чанка moov, содержащий track modification date
            str4 += moov['Data'][i]

    str = nibble_ret(int(str1, 16)) + nibble_ret(int(str2, 16)) + nibble_ret(int(str3, 16))
    if int(nibble_ret(int(str1, 16))[0]) >= 6:
        str += nibble_ret(int(str4, 16))

    reference_split = str[1:]
    nibbles = [nibble for nibble in reference_split.encode('ascii').hex()]
    return nibbles


def nibble_ret(sec: int) -> str:
    nibble_arr = []
    day = (sec // 86400) + 1
    sec = sec % 86400
    hour = sec // 3600
    sec = sec % 3600
    minutes = sec // 60
    seconds = sec % 60
    # Проверяем на наличие остатка в нибблах. В случае если при последнем переводе остается 1 ниббл, переводим только дни, если 2 - переводим дни и часы, и тд...
    if day > 0:
        nibble_arr.append(nibble2day_ret[day])
    if hour > 0:
        nibble_arr.append(nibble2hour_ret[hour])
    if minutes > 0:
        nibble_arr.append(nibble2minutes_ret[minutes])
    if seconds > 0:
        nibble_arr.append(nibble2seconds_ret[seconds])
    str = ''
    for i in range(len(nibble_arr)):
        str += nibble_arr[i]
    ans = bytes.fromhex(str).decode('UTF-8')
    return ans


def main_write(link: str, filepath: str, pathstego: str) -> None:
    write(link, filepath, pathstego)
    print('\033[31m' + 'Message has been interspersed successfully!' + '\033[0m')


def main_read(pathstego: str):
    return ex(read(pathstego))