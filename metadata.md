# <h1 align="center"> Метаданные в M4A

**Метаданные** — это набор следующих стандартизированных сведений о файле: имя автора, разрешение, цветовое пространство, авторские права и ключевые слова и т.д. Метаданные в M4A является сложной структурой, содержащей множество контейнеров и чанков.

Кол-во структур в метаданных M4A могут изменятся. Основные из них на схеме, представленной ниже.

  ![Схема чанков в метаданных](https://user-images.githubusercontent.com/59966999/217587566-66ee71ea-7cd7-49c7-964f-3cdd5ddccb79.png)
  
## **Moov (Movie Box)**

Эта коробка содержит информацию о метаданных для файловых носителей.
«Moov» - это контейнерная коробка, а конкретная информация содержимого интерпретируется подбором
 
### **Movie Header Box（mvhd）**



| Поле         | Байт |  Описание |
|--------------|:-----:|-----------:|
| box size |  4 |        Размер коробки |
| box type |  4 |          Тип коробки (mvhd) |
| version      |  1 |          Коробка версии, 0 или 1 |
| flags      |  3 |   В этом поле содержатся специфичные для процессора флаги, относящиеся к файлу.        |
| creation time |  4 |          Время создания (относительно времени UTC) |
| modification time |  4 |          Время изменения (относительно времени UTC) |
| time scale |  4 |          Значение масштаба файловой среды (можно понимать как количество единиц времени 1 секунды)|
| duration      |  4 |          Длина дорожки |
| rate      |  4 |          Рекомендуемая скорость воспроизведения (0x00010000 представляет собой нормальную игру) |
| volume      |  2 |           Громкость воспроизведения (0x0100 представляет максимальный объём)|
| reserved      |  10 |           Зарезервированная позиция)|
| matrix      |  36 |           Матрица, определяющая взаимосвязь между координатами в пространстве|
| preview time |  4 |           Просмотр времени; Начать предварительный просмотр этого времени файла|
| preview duration | 4 |           Проверка просмотра во временной шкале|
| poster time      |  4 |           |
| selection time | 4 |           Значение времени начала дорожки|
| selection duration | 4 |           |
| current time | 4 |           Текущее время|
| next track id | 4 |          Идентификационный номер, используемый следующим треком|

![Реальный пример mvhd](https://user-images.githubusercontent.com/59966999/217543973-595bab2e-73c2-412b-9c21-0d18c0761d19.png)


### **Track Box（trak)**
 
«TRAK» также является контейнерным ящиком

«Trak» должен содержать «TKHD» и «MDIA», из которых
«TKHD» - это коробка заголовка треков,
«MDIA» - это Media Box, которая является контейнером, содержащая некоторые панели информации о трековом медиа-данных.

### **Track Header Box（tkhd）**

| Поле         | Байт |  Описание |
|--------------|:-----:|-----------:|
| box size |  4 |        Размер коробки |
| box type |  4 |          Тип коробки (tkhd) |
| version      |  1 |          Коробка версии, 0 или 1 |
| flags      |  3 |       В этом поле содержатся специфичные для процессора флаги, относящиеся к файлу.    |
| creation time |  4 |          Время создания (относительно времени UTC) |
| modification time |  4 |          Время изменения (относительно времени UTC) |
|track id |  4 |          Идентификационный номер, не может повторяться и не 0|
| reserved      |  4 |           Зарезервированная позиция|
| duration      |  4 |         Длина отслеживания времени|
| reserved      |  8 |           Зарезервированная позиция|
| layer      |  2 |            Слой видео, по умолчанию 0, значение мало в верхнем слое|
| alternate group | 2 |           Информация о группе отслеживания, по умолчанию равно 0 указывает на то, что дорожка имеет групповые отношения с другим треком.|
| volume | 2 |           Формат, если звуковая дорожка, 1.0 (0x0100) представляет максимальный объем; в противном случае 0|
|reserved     |  2 |          Зарезервированная позиция |
| matrix | 36 |           Видео преобразование матрицы|
| width | 4 |           Ширина|
|  height | 4 |            Высота|

![Реальный пример tkhd](https://user-images.githubusercontent.com/59966999/217545546-5b73eb5b-c7c1-469e-845a-02f671fec533.png)


### **Media Box（mdia）**

«MDIA» также является контейнером, структура и виды их подкора более сложны.
Общие «MDIA» содержит:
«MDHD»,
«HDLR»,
«Minf»,
«UDTA»

среди них,
1. «MDHD» - это коробка для заголовков СМИ,
1. «HDLR» - это справочная коробка обработчика,
1. «Минф» - это ящик для медиа-информации,
1. «UDTA» - это коробка данных пользователя.



### **1.2.2.1 Media Header Box（mdhd)**

| Поле         | Байт |  Описание |
|--------------|:-----:|-----------:|
| box size |  4 |        Размер коробки |
| box type |  4 |          Тип коробки (mdhd) |
| version      |  1 |          Коробка версии, 0 или 1 |
| flags      |  3 |     В этом поле содержатся специфичные для процессора флаги, относящиеся к файлу.      |
| creation time |  4 |          Время создания (относительно времени UTC) |
| modification time |  4 |          Время изменения (относительно времени UTC) |
|time scale |  4 |          |
|duration |  4 |        Длина отслеживания времени  |
|language |  2 |      Медиавидный код. Самый высокий бит 0, а задняя часть - 3 символа (см. Определение ISO 639-2 / T).    |
|pre-defined |  2 |        |

![Реальный пример mdhd](https://user-images.githubusercontent.com/59966999/217546835-f93d3d1c-2466-4650-8b24-1dba44c8492b.png)


### **Handler Reference Box（hdlr）**
  
«HDLR» объясняет информацию о процессе воспроизведения СМИ, которая также может быть включена в Meta Box (META).

| Поле         | Байт |  Описание |
|--------------|:-----:|-----------:|
| box size |  4 |        Размер коробки |
| box type |  4 |          Тип коробки (hdlr) |
| version      |  1 |          Коробка версии, 0 или 1 |
| flags      |  3 |      В этом поле содержатся специфичные для процессора флаги, относящиеся к файлу.     |
| pre-defined |  4 |          |
|handler type|  4 |          В Media Box это значение составляет 4 символа: “vide”— video track; “soun”— audio track; “hint”— hint track |
|reserved |  12 |          Зарезервированная позиция |
|name |  неопределенный |          Имя типа трека, строка, заканчивая «\ 0» |



### **Media Information Box（minf）**
  
«Minf» хранит информацию о обработчике, которая объясняет данные трековых носителей, а обработчик медиа-обработчика использует эту информацию, чтобы сопоставить время носителя в носительские данные и процессы.

При нормальных обстоятельствах «Minf» содержит коробку заголовка, «Dinf» и «STBL», где

Коробка заголовка разделена на «SMHD», «HMHD» и «NMHD» в соответствии с типом трека (т.е. тип обработчика средств массовой информации).
«DINF» - это информация о данных,
«STBL» - это образца таблицы в таблице

**Sound Media Header Box（smhd)**

| Поле         | Байт |  Описание |
|--------------|:-----:|-----------:|
| box size |  4 |        Размер коробки |
| box type |  4 |          Тип коробки (smhd) |
| version      |  1 |          Коробка версии, 0 или 1 |
| flags      |  3 |           |
| balance |  2 |          |
| reserved |  2 | Зарезервированные поля, по умолчанию 0          |

![Реальный пример smhd](https://user-images.githubusercontent.com/59966999/217548777-cae25378-6125-4564-a876-0e0361e61038.png)


### **Data Information Box（dinf）**
  
«Dinf» объясняет, как найти информацию о медиа-информации - это контейнер.
«Dinf» обычно содержит «dref», а именно справочник данных;
«Dref» будет содержать несколько «URL» или «URN», который составляют таблицу, чтобы найти данные трека.

**dref**

| Поле         | Байт |  Описание |
|--------------|:-----:|-----------:|
| box size |  4 |        Размер коробки |
| box type |  4 |          Тип коробки (dref) |
| version      |  1 |          Коробка версии, 0 или 1 |
| flags      |  3 |     В этом поле содержатся специфичные для процессора флаги, относящиеся к файлу.      |
| entry count |  4 |       Количество элементов таблицы «URL» или «URN»   |
| Список «URL» или «URN» |  неопределённый | |

![Реальный пример dref](https://user-images.githubusercontent.com/59966999/217549265-023da315-637d-4541-a3a7-e6bea673c0ef.png)


### **Sample Table Box（stbl）**

«STBL» - это почти самая сложная коробка в обычном файле M4A
.
«STBL» - это контейнеровочная коробка, а его подкарые включает в себя:
sample description box（stsd）、
time to sample box（stts）、
Коробка размера выборки (STSZ или STZ2),
sample to chunk box（stsc）、
Коробка смещения Chunk (STCO или CO64),
composition time to sample box（ctts）、
Синхронизация образец коробки (STSS) и т. д.

### **Sample Description Box（stsd）**
  
В этом поле появится тип видео, широкая, длинная, длина, аудиоканал, выборка и т. Д.

| Поле         | Байт |  Описание |
|--------------|:-----:|-----------:|
| box size |  4 |        Размер коробки |
| box type |  4 |          Тип коробки (stsd) |
| version      |  1 |          Коробка версии, 0 или 1 |
| flags      |  3 |      В этом поле содержатся специфичные для процессора флаги, относящиеся к файлу.     |
| entry count |  4 |       Количество описаний образца   |
| Sample description |  неопределённый |Различные типы носителей имеют разное описание образца, но первые четыре поля каждого описания образца одинаковы, включая следующие элементы данных. |
| размер |  4 |       Количество байтов этого образца описания   |
| Формат данных |  4 |       Хранить формат данных  |
| reserved |  6 |       Зарезервированные поля, по умолчанию 0   |
| Ссылочный индекс данных |  2 |       Используйте этот индекс для получения данных, связанных с текущим описанием образца. Ссылки данных хранятся в данных справочных атомах   |

### **Time To Sample Box（stts）**
  
«STTS» хранит продолжительность образца, описывая метод отображения синхронизации образца, и мы можем найти любой раз образец времени.

### **Sample To Chunk Box（stsc）**
  
«STSC» описывает отображение образца и куска в «STSC», и посмотрите эту таблицу, чтобы найти Thunk, который указывает указанный образец, поэтому я нахожу этот образец.

### **Sample Size Box（stsz）**
  
«STSZ» определяет размер каждого образца, содержит количество всех образцов в носителях, а таблица дает каждый размер выборки. Эта коробка относительно велика.

| Поле         | Байт |  Описание |
|--------------|:-----:|-----------:|
| box size |  4 |        Размер коробки |
| box type |  4 |          Тип коробки (stsz) |
| version      |  1 |          Коробка версии, 0 или 1 |
| flags      |  3 |   В этом поле содержатся специфичные для процессора флаги, относящиеся к файлу.        |
|Sample size |  4 |      Количество всех образцов. Если вся образец имеет ту же длину, это поле это значение. В противном случае значение этого поля 0. Эти длины существуют в таблице размеров выборки  |
| entry count      |  3 |      Количество размеров выборки |
| sample size      |  неопределённое |      Структура таблицы размеров выборки. Эта таблица основана на индексе номера образца. Первый элемент является первым образцом, второй - второй образец |
| size      |  4 |      Каждый размер образца |

### **Chunk Offset Box（stco）**
  
«STCO» определяет местоположение каждого Thunk в медиа-потоке.

| Поле         | Байт |  Описание |
|--------------|:-----:|-----------:|
| box size |  4 |        Размер коробки |
| box type |  4 |          Тип коробки (stsz) |
| version      |  1 |          Коробка версии, 0 или 1 |
| flags      |  3 |    В этом поле содержатся специфичные для процессора флаги, относящиеся к файлу.       |
| entry count      |  4 |      Количество смещений куска |
| chunk offset |  3 |    неопределённое       |Смещение байта начинается из файла к текущему куску. Эта таблица основана на индексе номера Chunk. Первый элемент является первым стволом, второй элемент является вторым стволом|
| size      |  4 |      Каждый размер образца |
  
  
Использованные источники информации:
* https://russianblogs.com/article/37941959057/
* https://ru.wikipedia.org/wiki/MPEG-4_Part_14
* https://ru.bmstu.wiki/MPEG-4_Part_14
  




