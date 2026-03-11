import telebot

TOKEN = "8757297012:AAFycJjVLtGEQxp_WV8cz3VqLFOgEyImzCI"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"你好，我是烤冷面AI机器人 🍜")

@bot.message_handler(commands=['btc'])
def btc(message):
    bot.reply_to(message,"BTC 今日趋势：震荡偏多")

bot.infinity_polling()
