"""
Запись и чтение сообщения с сервиса privatty.py
Create at 27.02.2023 12:43:59
~core/privatty.py
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

import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import core.errors as errors


# по умолчанию на машине пользователя должен установлен браузер Chrome

class Privatty:
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # режим-призрак для браузера
    url_privatty = "https://privatty.com/ru/"

    @classmethod
    def write_message(cls, message: str) -> str:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=cls.chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get(cls.url_privatty)
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
    def read_message(cls, short_url: str) -> str:
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
        if driver.current_url == "https://privatty.com/ru/":
            raise errors.MessageHasAlreadyRead
        message = wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                             "sticker"
                                                             ))).text
        driver.quit()  # выход из веб-драйвера
        return message
