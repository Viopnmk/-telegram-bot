import telebot
import requests
import schedule
import time
import threading
import pandas as pd
import ta

TOKEN ="8757297012:AAFycJjVLtGEQxp_WV8cz3VqLFOgEyImzCI"
CHAT_ID =7637508163

bot = telebot.TeleBot(TOKEN)

# ======================
# 获取BTC价格
# ======================

def get_btc():

    try:

        url="https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        data=requests.get(url).json()

        return float(data["price"])

    except:

        return 0


# ======================
# 获取K线
# ======================

def get_klines():

    url="https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

    data=requests.get(url).json()

    close=[float(x[4]) for x in data]

    df=pd.DataFrame(close,columns=["close"])

    return df


# ======================
# RSI指标
# ======================

def get_rsi():

    df=get_klines()

    rsi=ta.momentum.RSIIndicator(df["close"]).rsi()

    return rsi.iloc[-1]


# ======================
# MACD指标
# ======================

def get_macd():

    df=get_klines()

    macd=ta.trend.MACD(df["close"])

    macd_line=macd.macd().iloc[-1]

    signal_line=macd.macd_signal().iloc[-1]

    if macd_line>signal_line:

        return "Bullish 📈"

    else:

        return "Bearish 📉"


# ======================
# 量化策略
# ======================

def quant_strategy():

    price=get_btc()

    rsi=get_rsi()

    macd=get_macd()

    if rsi<30:

        signal="可能超卖，考虑做多"

    elif rsi>70:

        signal="可能超买，注意回调"

    else:

        signal="市场中性"

    text=f"""
📊 BTC Quant Report

Price
${price}

RSI
{rsi:.2f}

MACD
{macd}

Strategy
{signal}
"""

    bot.send_message(CHAT_ID,text)


# ======================
# 手动命令
# ======================

@bot.message_handler(commands=['btc'])

def btc(message):

    price=get_btc()

    bot.reply_to(message,f"BTC价格 ${price}")


@bot.message_handler(commands=['quant'])

def quant(message):

    quant_strategy()


# ======================
# 自动推送
# ======================

schedule.every().hour.do(quant_strategy)


# ======================
# 运行定时任务
# ======================

def run_schedule():

    while True:

        schedule.run_pending()

        time.sleep(30)


threading.Thread(target=run_schedule).start()


# ======================
# 启动提示
# ======================

try:

    bot.send_message(CHAT_ID,"量化机器人启动成功 🤖")

except:

    pass


bot.infinity_polling()