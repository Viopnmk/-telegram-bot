import telebot
import requests

TOKEN = “8757297012:AAFycJjVLtGEQxp_WV8cz3VqLFOgEyImzCI”

bot = telebot.TeleBot(TOKEN)

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    data = requests.get(url).json()
    return data["bitcoin"]["usd"]

def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    data = requests.get(url).json()
    return data["ethereum"]["usd"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"🍜 烤冷面AI机器人已启动\n\n指令：\n/btc 查看BTC价格\n/eth 查看ETH价格")

@bot.message_handler(commands=['btc'])
def btc(message):
    price = get_btc_price()
    bot.reply_to(message,f"📈 BTC 实时价格\n\n${price}")

@bot.message_handler(commands=['eth'])
def eth(message):
    price = get_eth_price()
    bot.reply_to(message,f"📈 ETH 实时价格\n\n${price}")

bot.infinity_polling()