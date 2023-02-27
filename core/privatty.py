"""
Запись и чтение сообщения с сервиса privatty.py
Create at 27.02.2023 12:43:59
~privatty.py
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

import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# по умолчанию на машине пользователя должен установлен браузер Chrome

class Privatty:
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # режим-призрак для браузера
    url_privatty = "https://privatty.com/ru/"

    @classmethod
    def write_message(self, message: str) -> str:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get(self.url_privatty)
        driver.find_element(By.ID, "fld_note").click()  # нажимаем на textarea, чтобы активировать ввод текста
        driver.find_element(By.ID, "fld_note").send_keys(message)  # отправляем предварительно зашифрованное сообщение
        driver.find_element(By.ID, "creation_btn").click()  # создаём запись
        time.sleep(0.5)  # необходимая задержка для создания ссылки сервисом
        url = driver.find_element(By.ID, "privurl").get_property("value")
        driver.quit()  # выход из веб-драйвера
        return url

    @classmethod
    def read_message(self, short_url: str) -> str:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        driver.get(short_url)
        # нажимаем на кнопку "Да, показать запись"
        driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/div[3]/a[1]").click()
        time.sleep(1)  # необходимая задержка для того, чтобы считать сообщение
        message = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/div[2]").text
        driver.quit()  # выход из веб-драйвера
        return message
