##addtags.py - скрипт для добавления ID3 тегов в mp3-файлы.

###Использую для оформления подкастов.
----

**Особенности:**

- *ID3v2.3* для совместимости с Windows Media player и Windows Explorer
- Существующие теги переписываются
- Основные настройки в файле *settings.json* (находится в одном каталоге со скриптом)
- Обрабатывает все mp3-файлы в каталоге указанном первым параметром в коммандной строке или в текущем (без параметров)
- Shownotes берутся из txt-файлов одноименных mp3-файлам
- Скрипт определяет кодировку исходных файлов с shownotes и конвертирует в utf8
- Номер выпуска - первое число извлеченное из названия mp3-файла
- Название выпуска - имя файла, если в settings.json поле title=='', иначе высчитыватся eval (в моем случае к названию прибавляется номер выпуска)

**Requirements:**

- Python 2.7
- mutagen>=1.22