"""
Запись и чтение сообщения с сервиса privatty.py
Create at 27.02.2023 12:43:59
~core/sdarn/privatty.py
"""

import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import core.errors as errors
from core.sdarn.base import BaseSdarn
from core.cipher import *

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

Link = str
Message = str
Key = str
MaxLength = int
# по умолчанию на машине пользователя должен установлен браузер Chrome


class PrivattySdarn(BaseSdarn):
    _base_url = "https://privatty.com/ru/"
    name = 'privatty'
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # режим-призрак для браузера

    @classmethod
    def max_length(cls) -> MaxLength:
        """
        Возвращает максимальную длину возможного записываемого сообщения
        без учёта перевода в base64
        """
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=cls.chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get(cls._base_url)
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.element_to_be_clickable((By.ID, "fld_note")))
        if element.get_attribute("maxlength") is None:
            driver.quit()
            return 524288 # By default, the maximum of <textarea> in html 524288
        driver.quit()
        return element.get_attribute("maxlength")

    @classmethod
    def raw_write(cls, message: Message) -> Link:
        """
        Запись сообщения message и получениe ссылки
        """
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=cls.chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get(cls._base_url)
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.element_to_be_clickable((By.ID, "fld_note")))  # нажимаем на textarea, чтобы активировать ввод текста
        element.click()
        wait.until(EC.visibility_of_element_located((By.ID, "fld_note"))).send_keys(message)
        wait.until(EC.element_to_be_clickable((By.ID, "creation_btn"))).click()

        url = wait.until(EC.visibility_of_element_located((By.ID, "privurl"))).get_property("value")
        driver.quit()  # выход из веб-драйвера
        return url

    @classmethod
    def raw_read(cls, short_url: Link) -> Message:
        """
        Прочитать сообщение по ссылке,
        или вызвать ошибку, если его нет
        """
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=cls.chrome_options)
        wait = WebDriverWait(driver, 10)
        driver.get(short_url)
        try:
            if driver.find_element(By.CLASS_NAME, "code").text == '404':
                raise errors.WrongPassword
        except selenium.common.exceptions.NoSuchElementException:
            pass
        # нажимаем на кнопку "Да, показать запись"
        wait.until(EC.element_to_be_clickable((By.XPATH,
                                               "/html/body/div[1]/main/div/div/div[3]/a[1]"
                                               ))).click()
        if driver.current_url == cls._base_url:
            raise errors.MessageHasAlreadyRead
        message = wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                             "sticker"
                                                             ))).text
        driver.quit()  # выход из веб-драйвера
        return message

    @classmethod
    def write(cls, message: Message, key: Key) -> Link:
        """
        Проверка на длину сообщения, его шифрование и вызов функции raw_write
        """
        if len(message) + len(message) * 0.34 > cls.max_length(): # base64 увеличивает кол-во символов в 1/3 раза
            raise errors.LengthMassage("Количество символов должно быть равным " + str(cls.max_length()))
        if not cls.check_access():
            raise errors.ServiceError("Ошибка доступа к сервису")
        encrypted_massage = Cipher.encrypt_message(key,
                                                   message)  # шифруем сообщение через AES -> base64
        try:
            url = cls.raw_write(str(encrypted_massage)[2:-1])
            return url
        except selenium.common.exceptions.TimeoutException:
            raise errors.TimeError("Время запроса превышено!")

    @classmethod
    def read(cls, link: Link, key: Key) -> Message:
        """
        Вызов функции raw_read, расшифрование сообщения
        """
        assert isinstance(cls._base_url, str)
        assert link.startswith("https://goo.su/")

        encrypted_massage = cls.raw_read(link)
        bytes_ex_massage = bytes(encrypted_massage, encoding='utf-8')
        ex_massage = Cipher.decrypt_message(
            key,
            bytes_ex_massage
        )
        return str(ex_massage)[2:-1]


