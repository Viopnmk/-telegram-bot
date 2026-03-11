import requests

def btc_analysis():
    # ---------- 获取价格（带备用接口）----------
    price = None

    # 1. 尝试 Binance（正确接口）
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"   # 原第2行：修改为正确URL
        r = requests.get(url, timeout=10)
        data = r.json()
        if "price" in data:                     # 原第5行：改为判断存在性
            price = float(data["price"])
        else:
            raise ValueError("Binance 返回数据缺少 price")   # 原第6行：改为抛出异常
    except Exception as e:
        # 原第7行之后插入备用接口代码（第8行开始）
        # 2. 备用接口：CoinGecko
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            r = requests.get(url, timeout=10)
            data = r.json()
            price = float(data["bitcoin"]["usd"])
        except:
            # 3. 备用接口：OKX（可选，此处仅作示例，可自行添加）
            # 如果所有接口都失败，返回错误信息
            return "行情接口暂时不可用，请稍后再试"

    # 价格获取成功，继续分析（原第7行之后的代码移到这里，取消缩进）
    if price > 70000:
        trend = "强势上涨"
    elif price < 60000:
        trend = "弱势区间"
    else:
        trend = "震荡行情"

    return f"""
BTC快速分析

当前价格：
${price}

市场状态：
{trend}

建议：
关注关键突破
"""

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