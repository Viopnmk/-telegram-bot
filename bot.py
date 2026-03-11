import telebot
import requests
import schedule
import time
import threading

# =====================
# 填写你的信息
# =====================

TOKEN = "8757297012:AAFycJjVLtGEQxp_WV8cz3VqLFOgEyImzCI"
CHAT_ID =7637508163

bot = telebot.TeleBot(TOKEN)

# =====================
# 获取BTC价格
# =====================

def get_btc():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        data = requests.get(url).json()
        return float(data["price"])
    except:
        return 0


# =====================
# 获取ETH价格
# =====================

def get_eth():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
        data = requests.get(url).json()
        return float(data["price"])
    except:
        return 0


# =====================
# /start 指令
# =====================

@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(message,"机器人已启动 🚀")


# =====================
# BTC价格
# =====================

@bot.message_handler(commands=['btc'])
def btc(message):

    price = get_btc()

    bot.reply_to(message,f"BTC 价格: ${price}")


# =====================
# ETH价格
# =====================

@bot.message_handler(commands=['eth'])
def eth(message):

    price = get_eth()

    bot.reply_to(message,f"ETH 价格: ${price}")


# =====================
# 每日市场报告
# =====================

def market_report():

    btc = get_btc()

    eth = get_eth()

    text=f"""
📊 Daily Market Report

BTC
${btc}

ETH
${eth}
"""

    bot.send_message(CHAT_ID,text)


# =====================
# 定时任务
# =====================

schedule.every().day.at("08:00").do(market_report)


# =====================
# 运行定时任务
# =====================

def run_schedule():

    while True:

        schedule.run_pending()

        time.sleep(30)


threading.Thread(target=run_schedule).start()


# =====================
# 启动提示
# =====================

try:
    bot.send_message(CHAT_ID,"机器人启动成功 ✅")
except:
    pass


# =====================
# 启动机器人
# =====================

bot.infinity_polling()