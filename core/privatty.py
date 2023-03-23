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
    url_privatty = "https://safenote.co/"

    @classmethod
    def write_message(cls, message: str) -> str:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=cls.chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get(cls.url_privatty)
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.element_to_be_clickable((By.NAME, "note")))  # нажимаем на textarea, чтобы активировать ввод текста
        element.click()
        wait.until(EC.visibility_of_element_located((By.NAME, "note"))).send_keys(message)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="target"]/div[3]/div/div[2]/input'))).click()

        url = wait.until(EC.visibility_of_element_located((By.ID, 'link'))).get_property("value")
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
                raise errors.WrongPassword("В файл ничего не вкраплено либо пароль неверный!")
        except selenium.common.exceptions.NoSuchElementException:
            pass
        # нажимаем на кнопку "Да, показать запись"
        if driver.current_url == "https://safenote.co/expired":
            raise errors.MessageHasAlreadyRead("Сообщение было прочитано ранее")
        wait.until(EC.element_to_be_clickable((By.XPATH,
                                               '/html/body/div[2]/div/div/div/div/form/div[2]/div/div[2]/button'
                                               ))).click()

        message = wait.until(EC.presence_of_element_located((By.ID,
                                                             "note"
                                                             ))).text
        driver.quit()  # выход из веб-драйвера
        return message
