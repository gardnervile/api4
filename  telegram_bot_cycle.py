import os
import time
import random
import argparse
from telegram import Bot
from dotenv import load_dotenv
from PIL import Image
from tg_utils import send_photo_to_channel, get_images_from_directory


API_TOKEN = os.getenv["TG_TOKEN"]
bot = Bot(token=API_TOKEN)

CHANNEL_ID = os.environ["TG_CHANNEL_ID"]


def compress_image(image_path, max_size=20 * 1024 * 1024):
    image = Image.open(image_path)
    if os.path.getsize(image_path) > max_size:
        image = image.convert("RGB")
        compressed_path = f"compressed_{os.path.basename(image_path)}"
        image.save(compressed_path, optimize=True, quality=85)
        return compressed_path
    return image_path


def main(directory, interval):
    images = get_images_from_directory(directory)
    random.shuffle(images)

    while True:
        if not images:
            print("Все изображения опубликованы, перемешиваем заново...")
            images = get_images_from_directory(directory)
            random.shuffle(images)

        photo_path = os.path.join(directory, images.pop(0))
        print(f"Публикуем фото: {photo_path}")
        
        photo_path = compress_image(photo_path)

        send_photo_to_channel(bot, photo_path, CHANNEL_ID)

        print(f"Ждем {interval} секунд...")
        time.sleep(interval)


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Публикация фотографий в Telegram канал.")
    parser.add_argument("directory", help="Путь к директории с изображениями")
    parser.add_argument("-i", "--interval", type=int, default=int(os.getenv("PUBLISH_INTERVAL", 4 * 3600)), 
                        help="Задержка между публикациями в секундах (по умолчанию 4 часа)")

    args = parser.parse_args()
    main(args.directory, args.interval)
