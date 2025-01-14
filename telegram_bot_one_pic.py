import os
import random
from telegram import Bot
from dotenv import load_dotenv
import argparse
from tg_utils import send_photo_to_channel, get_images_from_directory

def publish_photo(directory, photo=None)
    bot = Bot(token=API_TOKEN)
    
    if not photo:
        photos = get_images_from_directory(directory)
        if not photos:
            raise FileNotFoundError("В директории нет фотографий для публикации.")
        photo = random.choice(photos)
    
    photo_path = os.path.join(directory, photo)
    send_photo_to_channel(bot, photo_path, CHANNEL_ID)

def handle_publish_error(e, photo=None):
    if isinstance(e, FileNotFoundError):
        print(f"Ошибка: Файл '{photo}' не найден.")
    elif isinstance(e, IsADirectoryError):
        print(f"Ошибка: '{photo}' является директорией, а не файлом.")
    elif isinstance(e, PermissionError):
        print(f"Ошибка: Нет прав на чтение файла '{photo}'.")

if __name__ == "__main__":
    load_dotenv()
    API_TOKEN = os.environ["TG_TOKEN"]
    CHANNEL_ID = os.environ["TG_CHANNEL_ID"]
    parser = argparse.ArgumentParser(description="Публикация фотографий в Telegram-канал.")
    parser.add_argument("directory", help="Директория с фотографиями.")
    parser.add_argument("-p", "--photo", help="Название фотографии для публикации.", default=None)

    args = parser.parse_args()

    try:
        publish_photo(args.directory, args.photo)
        print(f"Фотография '{args.photo}' успешно опубликована!")
    except (FileNotFoundError, IsADirectoryError, PermissionError) as e:
        handle_publish_error(e, args.photo)
