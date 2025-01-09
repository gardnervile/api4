from telegram import Bot


bot = Bot(token='8120078854:AAEHrDMF6tjno7si_qbdH_HdaKEfPObxV4A')

channel_id = '@picspace'

message = 'Привет! Это сообщение от бота.'

bot.send_message(chat_id=channel_id, text=message)