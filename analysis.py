import requests
import pandas as pd
import ta

def btc_analysis():

    try:

        url="https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

        r=requests.get(url,timeout=10)

        data=r.json()

        if not isinstance(data,list):

            return "K线数据获取失败"

        close=[]

        for i in data:

            if len(i)>4:

                close.append(float(i[4]))

        if len(close)<30:

            return "数据不足，无法分析"

        df=pd.DataFrame(close,columns=["close"])

        df["rsi"]=ta.momentum.RSIIndicator(df["close"]).rsi()

        macd=ta.trend.MACD(df["close"])

        df["macd"]=macd.macd()
        df["signal"]=macd.macd_signal()

        rsi=df["rsi"].iloc[-1]

        macd_value=df["macd"].iloc[-1]
        signal=df["signal"].iloc[-1]

        price=df["close"].iloc[-1]

        if rsi<30:

            trend="超卖可能反弹"

        elif rsi>70:

            trend="超买可能回调"

        else:

            trend="震荡"

        if macd_value>signal:

            macd_text="多头"

        else:

            macd_text="空头"

        return f"""
BTC技术分析

价格: ${price}

RSI: {round(rsi,2)}

MACD趋势: {macd_text}

市场状态: {trend}
"""

    except Exception as e:

        return f"分析失败: {e}"