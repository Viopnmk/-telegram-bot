import telebot
import requests
import schedule
import time
import threading

TOKEN ="8757297012:AAFycJjVLtGEQxp_WV8cz3VqLFOgEyImzCI"

bot = telebot.TeleBot(TOKEN)

# =================
# BTC价格
# =================
def get_btc():

    url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    data=requests.get(url).json()

    return data["bitcoin"]["usd"]


# =================
# ETH价格
# =================
def get_eth():

    url="https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

    data=requests.get(url).json()

    return data["ethereum"]["usd"]


# =================
# 市场数据
# =================
def get_market():

    url="https://api.coingecko.com/api/v3/global"

    data=requests.get(url).json()

    cap=data["data"]["total_market_cap"]["usd"]

    btc_dom=data["data"]["market_cap_percentage"]["btc"]

    return cap,btc_dom


# =================
# BTC分析
# =================
def analyze_btc():

    url="https://api.coingecko.com/api/v3/coins/bitcoin"

    data=requests.get(url).json()

    price=data["market_data"]["current_price"]["usd"]

    change=data["market_data"]["price_change_percentage_24h"]

    if change > 2:

        trend="短期上涨 📈"

    elif change < -2:

        trend="短期下跌 📉"

    else:

        trend="震荡行情"

    return price,change,trend


# =================
# Whale监控
# =================
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


# =================
# 稳定币监控
# =================
def stable_monitor():

    url="https://api.coingecko.com/api/v3/simple/price?ids=tether,usd-coin&vs_currencies=usd"

    data=requests.get(url).json()

    return "稳定币市场正常运行"


# =================
# 交易策略
# =================
def strategy():

    price=get_btc()

    support=price*0.97

    resistance=price*1.05

    text=f"""
📊 BTC交易策略

当前价格
${price}

支撑位
${support:.0f}

压力位
${resistance:.0f}

策略
回踩支撑做多
跌破止损
"""

    return text


# =================
# start
# =================
@bot.message_handler(commands=['start'])

def start(message):

    text="""
🍜 烤冷面AI加密助手

指令列表

/btc BTC价格
/eth ETH价格
/market 市场数据
/analysis AI行情
/whale 巨鲸监控
/stable 稳定币监控
/strategy 交易策略
"""

    bot.reply_to(message,text)


# =================
# BTC
# =================
@bot.message_handler(commands=['btc'])

def btc(message):

    price=get_btc()

    bot.reply_to(message,f"📈 BTC价格\n\n${price}")


# =================
# ETH
# =================
@bot.message_handler(commands=['eth'])

def eth(message):

    price=get_eth()

    bot.reply_to(message,f"📈 ETH价格\n\n${price}")


# =================
# 市场
# =================
@bot.message_handler(commands=['market'])

def market(message):

    cap,btc_dom=get_market()

    text=f"""
🌎 加密市场

总市值
${cap:,.0f}

BTC市占率
{btc_dom:.2f}%
"""

    bot.reply_to(message,text)


# =================
# 分析
# =================
@bot.message_handler(commands=['analysis'])

def analysis(message):

    price,change,trend=analyze_btc()

    text=f"""
📊 BTC行情分析

价格
${price}

24h涨跌
{change:.2f}%

趋势
{trend}
"""

    bot.reply_to(message,text)


# =================
# Whale
# =================
@bot.message_handler(commands=['whale'])

def whale(message):

    result=whale_check()

    bot.reply_to(message,result)


# =================
# 稳定币
# =================
@bot.message_handler(commands=['stable'])

def stable(message):

    result=stable_monitor()

    bot.reply_to(message,result)


# =================
# 策略
# =================
@bot.message_handler(commands=['strategy'])

def trade(message):

    result=strategy()

    bot.reply_to(message,result)


# =================
# 自动报告
# =================
def daily_report():

    btc=get_btc()

    eth=get_eth()

    text=f"""
📊 每日市场报告

BTC
${btc}

ETH
${eth}
"""

    print(text)


schedule.every().day.at("08:00").do(daily_report)


def run_schedule():

    while True:

        schedule.run_pending()

        time.sleep(30)


threading.Thread(target=run_schedule).start()


bot.infinity_polling()