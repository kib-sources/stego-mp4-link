"""
Запись и чтение сообщения с сервиса onetimesecret.py
Create at 04.05.2023 12:43:59
~core/sdarn/onetimesecret.py
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


class OneTimeSecretSdarn(BaseSdarn):
    _base_url = "https://onetimesecret.com/"
    name = 'onetimesecret'
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # режим-призрак для браузера

    @classmethod
    def max_length(cls) -> MaxLength:
        """
        возвращает максимальную длину возможного записываемого сообщения
        без учёта перевода в base64
        """
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=cls.chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get(cls._base_url)
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.element_to_be_clickable((
                By.NAME, "secret"
            )
            ))
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
            EC.element_to_be_clickable((By.NAME, "secret")))  # нажимаем на textarea, чтобы активировать ввод текста
        element.click()
        wait.until(EC.visibility_of_element_located((By.NAME, "secret"))).send_keys(message)
        wait.until(EC.element_to_be_clickable((By.NAME, "kind"))).click()
        url = wait.until(EC.visibility_of_element_located((By.ID, "secreturi"))).get_property("value")
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
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn'))).click()
        if driver.current_url == cls._base_url:
            raise errors.MessageHasAlreadyRead
        message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "input-block-level"))).text
        driver.quit()  # выход из веб-драйвера
        return message