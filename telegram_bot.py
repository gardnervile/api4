from telegram import Bot

# Ваш токен
bot = Bot(token='8120078854:AAEHrDMF6tjno7si_qbdH_HdaKEfPObxV4A')

# chat_id вашего канала
channel_id = '@picspace'

# Сообщение для отправки
message = 'Привет! Это сообщение от бота.'

# Отправка сообщения
bot.send_message(chat_id=channel_id, text=message)