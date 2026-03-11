import requests
import pandas as pd
import ta

def btc_analysis():

    try:

        url="https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

        r=requests.get(url)

        data=r.json()

        close=[float(i[4]) for i in data]

        df=pd.DataFrame(close,columns=["close"])

        df["rsi"]=ta.momentum.RSIIndicator(df["close"]).rsi()

        macd=ta.trend.MACD(df["close"])

        df["macd"]=macd.macd()

        df["signal"]=macd.macd_signal()

        rsi=df["rsi"].iloc[-1]

        macd_v=df["macd"].iloc[-1]

        signal=df["signal"].iloc[-1]

        if rsi<30:

            trend="超卖"

        elif rsi>70:

            trend="超买"

        else:

            trend="震荡"

        if macd_v>signal:

            macd_state="多头"

        else:

            macd_state="空头"

        return f"""
BTC技术分析

RSI: {round(rsi,2)}

MACD: {macd_state}

市场状态: {trend}
"""

    except Exception as e:

        return f"分析失败 {e}"