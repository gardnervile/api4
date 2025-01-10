import os
import random
from telegram import Bot
from dotenv import load_dotenv


load_dotenv()


API_TOKEN = os.getenv("TOKEN")
CHANNEL_ID = '@picspace'


bot = Bot(token=API_TOKEN)

def publish_photo(directory, photo=None):
    if not photo:
        photos = [file for file in os.listdir(directory) if file.endswith(('.jpg', '.jpeg', '.png'))]
        if not photos:
            print("В директории нет фотографий для публикации.")
            return
        photo = random.choice(photos)
    
    photo_path = os.path.join(directory, photo)
    try:
        with open(photo_path, 'rb') as file:
            bot.send_photo(chat_id=CHANNEL_ID, photo=file)
        print(f"Фотография '{photo}' успешно опубликована!")
    except Exception as e:
        print(f"Ошибка при публикации фотографии '{photo}': {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Публикация фотографий в Telegram-канал.")
    parser.add_argument("directory", help="Директория с фотографиями.")
    parser.add_argument("-p", "--photo", help="Название фотографии для публикации.", default=None)

    args = parser.parse_args()

    publish_photo(args.directory, args.photo)
