# <h1 align = "center">Стеганография в формате m4a


### Данный проект позволяет прятать информацию в формате .m4a

## Описание проекта

На сайте https://privnote.com/ мы оставляем секретное послание которое можно прочитать лишь один раз. Затем с помощью сайта https://clck.ru/ мы сокращаем ссылку, которую можем спрятать в данном звуковом формате. Так же в программе есть ключ-программа которая позволяет доствать спрятанные данные.

## Сценарий работы
Пример ссылки:
>https://clck.ru/33XgdY
> 
Из этой ссылки мы достаем 6 символов после знака "/". Затем с помощью библиотеки nibbles зашифровываем их в дни, часы, минуты и секунды. После находим количество секунд этих данных. Переводим это число в hex.

С помощью языка программирования python мы считываем hex код файла, доставая из него корневой атом moov. Далее в чанках mvhd и tkhd мы меняем данные Creation Time, Modification Time и Track Create Date  на данные которые мы получили из ссылки. После чего перезаписываем файл. Подробнее на схеме.

![Диаграмма без названия drawio](https://user-images.githubusercontent.com/59966999/218331729-e55ebdb3-122b-4f76-b4be-fb16f6ff1dd4.png)


## Как работает

Переходим в директорию с кодом при помощи команды cd <file path>.


![image_2023-02-14_00-25-53](https://user-images.githubusercontent.com/66170584/218578648-61f174c7-6cb9-437d-89c0-1c1b958799f4.png)

Далее чтобы вкраплять данные, в командной строке набираем команду:

```bash
~$ python3 poc_mp4_link.py --em https://clck.ru/<ваши6символов> --in <path *.m4a> --out <path *.m4a>
```

### Пример

```bash
~$ cd python3 poc_mp4_link.py --em https://clck.ru/33XgdY --in sample.m4a --out /home/kirill/poc/stego.m4a
```

![image_2023-02-14_00-27-00](https://user-images.githubusercontent.com/66170584/218578841-b655b055-cebb-4609-b1a4-1bbc97e8b9a7.png)

Чтобы извлечь данные, в командной строке набираем:

```bash
~$cd python3 poc_mp4_link.py --ex <PathToStego *.m4a>
```

### Пример 

```bash
~$ cd python3 poc_mp4_link.py --ex /home/kirill/poc/stego.m4a
```

![image_2023-02-14_00-27-31](https://user-images.githubusercontent.com/66170584/218578960-0049ccc3-277d-42c1-98f6-d8436f7b719c.png)



    
