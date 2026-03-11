import telebot
import requests
import schedule
import time
import threading

TOKEN ="8757297012:AAFycJjVLtGEQxp_WV8cz3VqLFOgEyImzCI"

bot = telebot.TeleBot(TOKEN)

# =====================
# 获取BTC价格
# =====================
def get_btc():
    url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    data=requests.get(url).json()
    return data["bitcoin"]["usd"]

# =====================
# 获取ETH价格
# =====================
def get_eth():
    url="https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    data=requests.get(url).json()
    return data["ethereum"]["usd"]

# =====================
# 获取市场数据
# =====================
def get_market():
    url="https://api.coingecko.com/api/v3/global"
    data=requests.get(url).json()

    cap=data["data"]["total_market_cap"]["usd"]
    btc_dom=data["data"]["market_cap_percentage"]["btc"]

    return cap,btc_dom

# =====================
# BTC分析
# =====================
def analyze_btc():

    url="https://api.coingecko.com/api/v3/coins/bitcoin"

    data=requests.get(url).json()

    price=data["market_data"]["current_price"]["usd"]

    change=data["market_data"]["price_change_percentage_24h"]

    if change > 2:
        trend="短期上涨趋势 📈"

    elif change < -2:
        trend="短期下跌趋势 📉"

    else:
        trend="震荡行情"

    return price,change,trend

# =====================
# Whale监控
# =====================
def whale_check():

    url="https://api.whale-alert.io/v1/transactions?api_key=demo&min_value=5000000"

    data=requests.get(url).json()

    if "transactions" in data and len(data["transactions"])>0:

        tx=data["transactions"][0]

        amount=tx["amount"]

        coin=tx["symbol"]

        return f"🐳 巨鲸转账\n\n{amount} {coin}"

    else:

        return "暂无巨鲸转账"

# =====================
# start
# =====================
@bot.message_handler(commands=['start'])

def start(message):

    text="""
🍜 烤冷面AI加密助手

指令：

/btc BTC价格
/eth ETH价格
/market 市场数据
/analysis BTC分析
/news 市场新闻
/whale 巨鲸监控
"""

    bot.reply_to(message,text)

# =====================
# BTC
# =====================
@bot.message_handler(commands=['btc'])

def btc(message):

    price=get_btc()

    bot.reply_to(message,f"📈 BTC价格\n\n${price}")

# =====================
# ETH
# =====================
@bot.message_handler(commands=['eth'])

def eth(message):

    price=get_eth()

    bot.reply_to(message,f"📈 ETH价格\n\n${price}")

# =====================
# 市场
# =====================
@bot.message_handler(commands=['market'])

def market(message):

    cap,btc_dom=get_market()

    text=f"""
🌎 加密市场

总市值: ${cap:,.0f}

BTC市占率: {btc_dom:.2f}%
"""

    bot.reply_to(message,text)

# =====================
# AI分析
# =====================
@bot.message_handler(commands=['analysis'])

def analysis(message):

    price,change,trend=analyze_btc()

    text=f"""
📊 BTC AI行情分析

价格: ${price}

24h涨跌: {change:.2f}%

趋势: {trend}
"""

    bot.reply_to(message,text)

# =====================
# 新闻
# =====================
@bot.message_handler(commands=['news'])

def news(message):

    bot.reply_to(message,"📰 今日市场\n\nETF资金持续流入\n机构增持BTC")

# =====================
# Whale
# =====================
@bot.message_handler(commands=['whale'])

def whale(message):

    result=whale_check()

    bot.reply_to(message,result)

# =====================
# 自动报告
# =====================
def daily_report():

    btc=get_btc()

    eth=get_eth()

    text=f"""
📊 每日市场报告

BTC: ${btc}

ETH: ${eth}

市场整体：震荡
"""

    print(text)

schedule.every().day.at("08:00").do(daily_report)

def run_schedule():

    while True:

        schedule.run_pending()

        time.sleep(30)

threading.Thread(target=run_schedule).start()

# =====================
# 启动机器人
# =====================
bot.infinity_polling()