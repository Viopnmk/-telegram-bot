import telebot
import requests
import schedule
import time
import pandas as pd
import ta
import threading

TOKEN="8757297012:AAFycJjVLtGEQxp_WV8cz3VqLFOgEyImzCI"
CHAT_ID=7637508163

bot=telebot.TeleBot(TOKEN)

# 获取BTC价格
def get_btc_price():

    url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    data=requests.get(url).json()

    return data["bitcoin"]["usd"]

# 获取K线数据
def get_kline():

    url="https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

    data=requests.get(url).json()

    close=[float(i[4]) for i in data]

    df=pd.DataFrame(close,columns=["close"])

    return df

# 技术分析
def analyze():

    df=get_kline()

    df["rsi"]=ta.momentum.RSIIndicator(df["close"]).rsi()

    macd=ta.trend.MACD(df["close"])

    df["macd"]=macd.macd()
    df["signal"]=macd.macd_signal()

    rsi=df["rsi"].iloc[-1]

    macd_value=df["macd"].iloc[-1]
    signal=df["signal"].iloc[-1]

    price=df["close"].iloc[-1]

    trend="震荡"

    if rsi<30:
        trend="超卖可能反弹"

    if rsi>70:
        trend="超买可能回调"

    if macd_value>signal:
        macd_text="多头趋势"

    else:
        macd_text="空头趋势"

    return f"""
BTC价格: ${price}

RSI: {round(rsi,2)}
MACD: {macd_text}

市场判断:
{trend}
"""

# /start
@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(message,"量化机器人启动成功 🤖")

# /btc
@bot.message_handler(commands=['btc'])
def btc(message):

    price=get_btc_price()

    bot.reply_to(message,f"BTC实时价格: ${price}")

# /analysis
@bot.message_handler(commands=['analysis'])
def analysis(message):

    result=analyze()

    bot.reply_to(message,result)

# 自动推送
def push():

    result=analyze()

    bot.send_message(CHAT_ID,"📊 每小时BTC分析\n"+result)

schedule.every(1).hours.do(push)

# 定时线程
def run_schedule():

    while True:

        schedule.run_pending()
        time.sleep(10)

threading.Thread(target=run_schedule).start()

print("机器人运行成功")

bot.infinity_polling()