# Фото космоса

Этот проект позволяет собирать фотографии с разных источников (NASA APOD, EPIC, SpaceX) и публиковать их в Telegram-канале.

## Описание скриптов

- fetch_apod_images.py
  
Скрипт для скачивания изображений из NASA Astronomy Picture of the Day (APOD). Загружает картинку за сегодняшний день или за указанную дату.

Использование:
```
python3 fetch_apod_images.py --date YYYY-MM-DD
```
- fetch_epic_images.py
  
Скрипт для скачивания изображений с NASA EPIC (Earth Polychromatic Imaging Camera). Изображения планеты Земля с орбиты.

Использование:
```
python3 fetch_epic_images.py
```
- fetch_spacex_images.py
  
Скрипт для получения изображений с запусков SpaceX.

Использование:
```
python3 fetch_spacex_images.py --id <launch_id>
```
- telegram_bot.py

Скрипт для создания бота в Telegram, который публикует изображения в канал.

Использование:
```
python telegram_bot.py /path/to/images -i 14400
```
- telegram_bot_one_pic.py

Этот скрипт публикует фотографию в Telegram-канал. Пользователь может указать конкретный файл для публикации или оставить выбор на усмотрение скрипта — тогда будет опубликована случайная фотография из указанной директории.

Использование:
```
python3 telegram_bot_one_pic.py /path/to/photo.jpg
```
-отправка конкретной фотографии
```
python3 telegram_bot_one_pic.py /path/to/directory
```
-отправка случайной фотографии из директории

## Для работы скриптов потребуется установить следующие библиотеки:
```
pip install -r requirements.txt
```
## Переменные окружения

Скрипт требует настройки переменной окружения для API-токена Telegram:

```
TG_TOKEN=your_telegram_bot_token
TG_CHANNEL_ID=@your_tg_channel
NASA_API_KEY=your_api_key
PUBLISH_INTERVAL=14400 
```
