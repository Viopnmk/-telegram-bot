import telebot
from config import TOKEN
from market import btc_price, eth_price
from analysis import btc_analysis
from whale import whale_alert
from news import crypto_news

bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(message,"量化机器人启动成功 🤖")

@bot.message_handler(commands=['btc'])
def btc(message):

    price=btc_price()

    bot.reply_to(message,f"BTC价格: ${price}")

@bot.message_handler(commands=['eth'])
def eth(message):

    price=eth_price()

    bot.reply_to(message,f"ETH价格: ${price}")

@bot.message_handler(commands=['market'])
def market(message):

    text=market_data()

    bot.reply_to(message,text)

@bot.message_handler(commands=['analysis'])
def analysis(message):

    bot.reply_to(message,"正在分析市场...")

    result=btc_analysis()

    bot.send_message(message.chat.id,result)

@bot.message_handler(commands=['whale'])
def whale(message):

    text=whale_alert()

    bot.reply_to(message,text)

@bot.message_handler(commands=['news'])
def news(message):

    text=crypto_news()

    bot.reply_to(message,text)

bot.infinity_polling()