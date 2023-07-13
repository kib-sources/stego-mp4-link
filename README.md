<h1>Stego-mp4-link</h1>

Ссылочная стеганография в метаданных *.m4a файлов

## Содержание
- [Технологии](#технологии)
- [Требования](#требования)
- [Установка пакетов](#установка-пакетов)
- [Получение API-токена](#получение-токена)
- [Примеры использования](#примеры-использования)
- [Тестирование](#тестирование)
- [Команда проекта](#команда-проекта)


## Технологии

- <a href="https://www.selenium.dev/documentation/">Selenium</a>
- <a href="https://pypi.org/project/pycryptodomex/">PyCryptoDomex</a>

## Требования

- OS Linux
- Google Chrome (Chromium)
- Доступ в Интернет
- Python3
- Pip

## Установка пакетов
```sh
~$ python3 -m venv venv
~$ source venv/bin/activate
(venv) ~$ pip install -r requirements.txt
```

## Получение токена
1) Создаём файл .env
```sh
(venv) ~$ touch .env
```
2) Для получения личного токена необходимо зарегистрироваться на https://goo.su/, перейти на вкладку API, получить токен.

![image](https://github.com/kib-sources/stego-mp4-link/assets/59966999/1f776376-cd5c-47b1-a374-3d6afbfcb7cf)

3) Скопировать ключ в переменную `API_TOKEN` в файле .env (см. пример в .env.example).
```sh
API_TOKEN='wi**********************************************' (полученный API токен)
```


## Примеры использования

Запись зашифрованного сообщения, используя сервисы одноразовых записок https://privatty.com и сокращения ссылок https://goo.su

```sh
(venv) ~$ python -m stego --em -p VeRy$ecrEtPa$$woRD -m MyMessage -i poc/sample.m4a -o poc/stego.m4a
```

Получение сообщения, используя сервисы одноразовых записок https://privatty.com и сокращения ссылок https://goo.su

```sh
(venv) ~$ python -m stego --em --ex -p VeRy$ecrEtPa$$woRD -i poc/stego.m4a
```

## Тестирование

<p>Наш проект использует unit-test python.</p>

Тест записи и чтения, используя сервис одноразовых записок https://onetimesecret.com

```sh
(venv) ~$cd tests;python -m unittest test_work_with_m4a_onetimesecret.TestMain
```

Тест записи и чтения, используя сервис одноноразовых записок https://privatty.com

```sh
(venv) ~$cd tests;python -m unittest test_work_with_m4a_privatty.TestMain
```

## Команда проекта
<a href="https://github.com/yourProgrammist">Осин Кирилл</a>

<a href="https://github.com/nurovAm">Нуров Амир</a>

По вопросам и предложениям писать - https://t.me/osin_hjj (Кирилл),  https://t.me/Amir_Nurov (Амир)
