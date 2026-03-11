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

    url="https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    data=requests.get(url).json()

    return float(data["price"])


# ======================
# 获取ETH价格
# ======================

def get_eth():

    url="https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

    data=requests.get(url).json()

    return float(data["price"])


# ======================
# 获取K线数据
# ======================

def get_klines():

    url="https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

    data=requests.get(url).json()

    close=[float(x[4]) for x in data]

    df=pd.DataFrame(close,columns=["close"])

    return df


# ======================
# RSI计算
# ======================

def rsi_signal():

    df=get_klines()

    rsi=ta.momentum.RSIIndicator(df["close"]).rsi()

    last=rsi.iloc[-1]

    if last>70:
        return "超买 📉"

    elif last<30:
        return "超卖 📈"

    else:
        return "中性"


# ======================
# MACD计算
# ======================

def macd_signal():

    df=get_klines()

    macd=ta.trend.MACD(df["close"])

    macd_line=macd.macd().iloc[-1]

    signal_line=macd.macd_signal().iloc[-1]

    if macd_line>signal_line:

        return "多头趋势 📈"

    else:

        return "空头趋势 📉"


# ======================
# 交易策略
# ======================

def trading_strategy():

    price=get_btc()

    rsi=rsi_signal()

    macd=macd_signal()

    support=price*0.97

    resistance=price*1.05

    text=f"""

📊 BTC Quant Strategy

Price
${price}

Support
${support:.0f}

Resistance
${resistance:.0f}

RSI
{rsi}

MACD
{macd}

"""

    bot.send_message(CHAT_ID,text)


# ======================
# 市场报告
# ======================

def market_report():

    btc=get_btc()

    eth=get_eth()

    text=f"""

📊 Daily Market Report

BTC
${btc}

ETH
${eth}

"""

    bot.send_message(CHAT_ID,text)


# ======================
# 巨鲸监控
# ======================

def whale_alert():

    url="https://api.whale-alert.io/v1/transactions?api_key=demo&min_value=5000000"

    data=requests.get(url).json()

    if "transactions" in data:

        tx=data["transactions"][0]

        amount=tx["amount"]

        coin=tx["symbol"]

        text=f"""

🐳 Whale Alert

{amount} {coin}

Large transfer detected
"""

        bot.send_message(CHAT_ID,text)


# ======================
# 定时任务
# ======================

schedule.every().day.at("08:00").do(market_report)

schedule.every().day.at("12:00").do(trading_strategy)

schedule.every(15).minutes.do(whale_alert)


# ======================
# 启动调度
# ======================

def run_schedule():

    while True:

        schedule.run_pending()

        time.sleep(30)

threading.Thread(target=run_schedule).start()

bot.infinity_polling()

@bot.message_handler(commands=['test'])
def test(message):

    bot.reply_to(message,"机器人正常运行 ✅")