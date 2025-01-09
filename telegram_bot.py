from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TOKEN")

channel_id = '@picspace'

bot = Bot(token=API_TOKEN)

photo_path = '/Users/evgenijkondratev/Desktop/api4/nasa_apod_images/apod_image_3.jpg'

bot.send_photo(chat_id=channel_id, photo=open(photo_path, 'rb'))