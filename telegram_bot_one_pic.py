import os
import random
import argparse
from telegram import Bot
from dotenv import load_dotenv
from tg_utils import get_images_from_directory, send_photo_to_channel


def publish_photo(bot, directory, photo=None, channel_id):
    if photo:
        photo_path = photo
    else:
        photos = get_images_from_directory(directory)
        if not photos:
            raise FileNotFoundError("В директории нет фотографий для публикации.")
        photo_path = os.path.join(directory, random.choice(photos))

    send_photo_to_channel(bot, photo_path, channel_id)
    return os.path.basename(photo_path)


def handle_publish_error(e, photo=None):
    if isinstance(e, FileNotFoundError):
        print(f"Ошибка: {str(e)}")
    elif isinstance(e, NotADirectoryError):
        print(f"Ошибка: {str(e)}")
    elif isinstance(e, PermissionError):
        print(f"Ошибка: Нет прав на чтение файла '{photo}'.")


def main():
    load_dotenv()
    api_token = os.getenv("TG_TOKEN")
    channel_id = os.getenv("TG_CHANNEL_ID")
    
    if not api_token:
        raise ValueError("TG_TOKEN должен быть установлен в переменных окружения.")
    if not channel_id:
        raise ValueError("TG_CHANNEL_ID должен быть установлен в переменных окружения.")
    
    parser = argparse.ArgumentParser(description="Публикация фотографий в Telegram-канал.")
    parser.add_argument("path", help="Путь к фотографии или директории.")
    parser.add_argument("-p", "--photo", help="Название фотографии для публикации.", default=None)

    args = parser.parse_args()

    if os.path.isfile(args.path):
        directory = os.path.dirname(args.path)
        photo = args.path
    elif os.path.isdir(args.path):
        directory = args.path
        photo = args.photo
    else:
        raise FileNotFoundError(f"Путь '{args.path}' не найден или не является файлом/директорией.")
    
    bot = Bot(token=api_token)

    try:
        print(f"Публикуем {'файл' if photo else 'случайную фотографию'} из директории: {directory}")
        published_photo = publish_photo(bot, directory, photo=photo, channel_id=channel_id)
        print(f"Фотография '{published_photo}' успешно опубликована!")
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        handle_publish_error(e, photo)


if __name__ == "__main__":
    main()
