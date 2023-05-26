<h1>Stego-mp4-link</h1>

Ссылочная стеганография в метаданных *.m4a файлов

## Содержание
- [Технологии](#технологии)
- [Требования](#требования)
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

## Примеры использования

Запись зашифрованного сообщения, используя сервисы одноразовых записок https://privatty.com и сокращения ссылок https://goo.su

```sh
python3 stego.py --em -p VeRy$ecrEtPa$$woRD -m MyMessage -i poc/sample.m4a -o poc/stego.m4a
```

Получение сообщения, используя сервисы одноразовых записок https://privatty.com и сокращения ссылок https://goo.su

```sh
python3 stego.py --ex -p VeRy$ecrEtPa$$woRD -i poc/stego.m4a
```

## Тестирование

<p>Наш проект использует unit-test python.</p>

Тест записи и чтения, используя сервис одноразовых записок https://onetimesecret.com

```sh
cd tests;python3 -m unittest test_work_with_m4a_onetimesecret.TestMain
```

Тест записи и чтения, используя сервис одноноразовых записок https://privatty.com

```sh
cd tests;python3 -m unittest test_work_with_m4a_privatty.TestMain
```

## Команда проекта
<a href="https://github.com/yourProgrammist">Осин Кирилл</a>

<a href="https://github.com/nurovAm">Нуров Амир</a>
