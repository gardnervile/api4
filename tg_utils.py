import os
from telegram import Bot

def send_photo_to_channel(bot, photo_path, channel_id):
    with open(photo_path, 'rb') as file:
        bot.send_photo(chat_id=channel_id, photo=file)

def get_images_from_directory(directory, extensions=('jpg', 'jpeg', 'png', 'gif')):
    return [f for f in os.listdir(directory) if f.lower().endswith(extensions)]
