import os
import random
import argparse
from telegram import Bot
from dotenv import load_dotenv
from tg_utils import get_images_from_directory


def publish_photo(directory, photo=None, api_token=None, channel_id=None):
    bot = Bot(token=api_token)
    
    if photo:
        photo_path = photo
        if not os.path.isfile(photo_path):
            raise FileNotFoundError(f"Файл '{photo}' не найден.")
    else:
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"'{directory}' не является директорией.")
        photos = get_images_from_directory(directory)
        if not photos:
            raise FileNotFoundError("В директории нет фотографий для публикации.")
        photo_path = os.path.join(directory, random.choice(photos))

    with open(photo_path, 'rb') as photo_file:
        bot.send_photo(chat_id=channel_id, photo=photo_file)
    
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
    api_token = os.environ["TG_TOKEN"]
    channel_id = os.environ["TG_CHANNEL_ID"]
    
    parser = argparse.ArgumentParser(description="Публикация фотографий в Telegram-канал.")
    parser.add_argument("path", help="Путь к фотографии или директории.")
    parser.add_argument("-p", "--photo", help="Название фотографии для публикации.", default=None)

    args = parser.parse_args()

    if os.path.isfile(args.path):
        directory = os.path.dirname(args.path)
        photo = args.path
    else:
        directory = args.path
        photo = args.photo

    try:
        publish_photo_lambda = lambda: publish_photo(directory, photo, api_token=api_token, channel_id=channel_id)
        
        if photo:
            print(f"Публикуем файл: {photo}")
        else:
            print(f"Публикуем случайную фотографию из директории: {directory}")
        
        published_photo = publish_photo_lambda()
        print(f"Фотография '{published_photo}' успешно опубликована!")
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        handle_publish_error(e, photo)


if __name__ == "__main__":
    main()
