import telebot

BOT_TOKEN = "8278199186:AAH_Wj-Xgb__cPZNIblLppDKvqAZvY8Jcj8"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Бот работает!")

bot.polling()
