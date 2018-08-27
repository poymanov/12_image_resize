# Image Resizer

Скрипт изменяет размер указанного изображения.

Режимы работы:
- Увеличить масштаб
- Изменить размер на конкретно указанный
- Изменить размер по ширине или высоте с сохранением пропорций исходного изображения


# Предварительные настройки

- Установить и запустить [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) для Python
- Установить дополнительные пакеты:
```
pip install -r requirements.txt
```

# Как запустить

Скрипт требует для своей работы установленного интерпретатора **Python** версии **3.5**.

**Запуск на Linux**

```bash
# запуск в режиме увеличения масштаба
$ python image_resize.py <path_to_file> --scale 2 # или python3, в зависимости от настроек системы

# запуск в режиме изменения размера до указанных значений
$ python image_resize.py <path_to_file> --width 100 --height 100

# скрипт выведет предупреждение, если пропорции нового изображения нарушены
Attention! The proportions of the new image do not match the proportions of the original

# запуск в режиме изменения размера по ширине
$ python image_resize.py <path_to_file> --width 100

# запуск в режиме изменения размера по высоте
$ python image_resize.py <path_to_file> --height 100

# в случае успешного сохранения, скрипт выведет путь размещения измененного файла
Resized file saved to: test__1440x960.jpg

# по-умолчанию файл сохраняется в директории проекта,
# можно указать другой путь для сохранения (он должен существовать)
$ python image_resize.py <path_to_file> --scale 2 --output ./test

```

Запуск на **Windows** происходит аналогично.

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)
