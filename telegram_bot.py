from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))

channel_id = '@picspace'

message = 'Привет! Это сообщение от бота.'

bot.send_message(chat_id=channel_id, text=message)