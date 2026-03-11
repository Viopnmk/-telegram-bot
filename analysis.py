import requests
import pandas as pd
import ta

def btc_analysis():

    url="https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

    r=requests.get(url,timeout=10)

    data=r.json()

    close=[float(i[4]) for i in data]

    df=pd.DataFrame(close,columns=["close"])

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
BTC技术分析

价格:
${price}

RSI:
{round(rsi,2)}

MACD:
{macd_text}

趋势判断:
{trend}
"""