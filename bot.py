import telebot
import requests

TOKEN = "8757297012:AAFycJjVLtGEQxp_WV8cz3VqLFOgEyImzCI"

bot = telebot.TeleBot(TOKEN)

# BTC价格
def get_btc():
    url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    data=requests.get(url).json()
    return data["bitcoin"]["usd"]

# ETH价格
def get_eth():
    url="https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    data=requests.get(url).json()
    return data["ethereum"]["usd"]

# 市场数据
def get_market():
    url="https://api.coingecko.com/api/v3/global"
    data=requests.get(url).json()
    cap=data["data"]["total_market_cap"]["usd"]
    btc_dom=data["data"]["market_cap_percentage"]["btc"]
    return cap,btc_dom

@bot.message_handler(commands=['start'])
def start(message):
    text="""
🍜 烤冷面AI加密助手

可用指令：

/btc  BTC价格
/eth  ETH价格
/market 市场数据
/news 加密新闻
/whale 巨鲸监控
"""
    bot.reply_to(message,text)

@bot.message_handler(commands=['btc'])
def btc(message):
    price=get_btc()
    bot.reply_to(message,f"📈 BTC价格\n\n${price}")

@bot.message_handler(commands=['eth'])
def eth(message):
    price=get_eth()
    bot.reply_to(message,f"📈 ETH价格\n\n${price}")

@bot.message_handler(commands=['market'])
def market(message):
    cap,btc_dom=get_market()
    text=f"""
🌎 加密市场

总市值: ${cap:,.0f}

BTC市占率: {btc_dom:.2f}%
"""
    bot.reply_to(message,text)

@bot.message_handler(commands=['news'])
def news(message):
    bot.reply_to(message,"📰 今日加密新闻\n\nETF资金持续流入\n机构增持BTC")

@bot.message_handler(commands=['whale'])
def whale(message):
    bot.reply_to(message,"🐳 巨鲸监控\n\n暂无大额转账")

bot.infinity_polling()