import os
import random
import asyncio
from telegram import Bot
from dotenv import load_dotenv
import argparse
from tg_utils import send_photo_to_channel, get_images_from_directory


async def publish_photo(directory, photo=None, get_credentials=None):
    api_token, channel_id = get_credentials()

    bot = Bot(token=api_token)
    
    if photo:
        photo_path = os.path.join(directory, photo)
        if not os.path.isfile(photo_path):
            raise FileNotFoundError(f"Файл '{photo}' не найден в директории '{directory}'.")
    else:
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"'{directory}' не является директорией.")
        photos = get_images_from_directory(directory)
        if not photos:
            raise FileNotFoundError("В директории нет фотографий для публикации.")
        photo_path = os.path.join(directory, random.choice(photos))
    with open(photo_path, 'rb') as photo_file:
        await bot.send_photo(chat_id=channel_id, photo=photo_file)

        
def handle_publish_error(e, photo=None):
    if isinstance(e, FileNotFoundError):
        print(f"Ошибка: Файл '{photo}' не найден.")
    elif isinstance(e, IsADirectoryError):
        print(f"Ошибка: '{photo}' является директорией, а не файлом.")
    elif isinstance(e, PermissionError):
        print(f"Ошибка: Нет прав на чтение файла '{photo}'.")
    elif isinstance(e, NotADirectoryError):
        print(f"Ошибка: '{photo}' не является директорией.")

async def main():
    load_dotenv()

    get_credentials = lambda: (os.environ["TG_TOKEN"], os.environ["TG_CHANNEL_ID"])
    
    parser = argparse.ArgumentParser(description="Публикация фотографий в Telegram-канал.")
    parser.add_argument("directory", help="Директория с фотографиями.")
    parser.add_argument("-p", "--photo", help="Название фотографии для публикации.", default=None)

    args = parser.parse_args()

    try:
        if args.photo:
            print(f"Публикуем файл: {args.photo}")
        else:
            print(f"Публикуем случайную фотографию из директории: {args.directory}")
        
        await publish_photo(args.directory, args.photo, get_credentials=get_credentials)
        print(f"Фотография '{args.photo}' успешно опубликована!")
    except (FileNotFoundError, IsADirectoryError, PermissionError, NotADirectoryError) as e:
        handle_publish_error(e, args.photo)


if __name__ == "__main__":
    asyncio.run(main())
