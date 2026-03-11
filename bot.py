import telebot
import requests
import pandas as pd
import ta

TOKEN="8757297012:AAFycJjVLtGEQxp_WV8cz3VqLFOgEyImzCI"

bot=telebot.TeleBot(TOKEN)

# 获取BTC价格
def get_btc():

    url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    data=requests.get(url).json()

    return data["bitcoin"]["usd"]

# 获取ETH价格
def get_eth():

    url="https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

    data=requests.get(url).json()

    return data["ethereum"]["usd"]

# 获取市场数据
def get_market():

    url="https://api.coingecko.com/api/v3/global"

    data=requests.get(url).json()

    cap=data["data"]["total_market_cap"]["usd"]

    btc_dom=data["data"]["market_cap_percentage"]["btc"]

    return cap,btc_dom


# 获取K线
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

    result=f"""
BTC技术分析

价格: ${price}

RSI: {round(rsi,2)}

MACD: {macd_text}

市场判断:
{trend}
"""

    return result


# start
@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(message,"量化机器人启动成功 🤖")


# btc
@bot.message_handler(commands=['btc'])
def btc(message):

    price=get_btc()

    bot.reply_to(message,f"BTC价格: ${price}")


# eth
@bot.message_handler(commands=['eth'])
def eth(message):

    price=get_eth()

    bot.reply_to(message,f"ETH价格: ${price}")


# market
@bot.message_handler(commands=['market'])
def market(message):

    cap,btc_dom=get_market()

    text=f"""
加密市场数据

总市值:
${cap}

BTC占比:
{btc_dom}%
"""

    bot.reply_to(message,text)


# analysis
@bot.message_handler(commands=['analysis'])
def analysis(message):

    bot.reply_to(message,"正在分析市场...")

    result=analyze()

    bot.send_message(message.chat.id,result)


# news
@bot.message_handler(commands=['news'])
def news(message):

    text="""
今日加密新闻

BTC ETF资金流增加
机构持续买入

市场情绪:
偏多
"""

    bot.reply_to(message,text)


# whale
@bot.message_handler(commands=['whale'])
def whale(message):

    text="""
巨鲸监控

5000 BTC
转入交易所

可能存在卖压
"""

    bot.reply_to(message,text)


print("机器人启动成功")

bot.infinity_polling()