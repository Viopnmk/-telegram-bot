import requests

def btc_analysis():

    try:

        url="https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        r=requests.get(url,timeout=10)

        data=r.json()

        if "price" not in data:

            return "行情接口暂时不可用，请稍后再试"

        price=float(data["price"])

        if price>70000:
            trend="强势上涨"
        elif price<60000:
            trend="弱势区间"
        else:
            trend="震荡行情"

        return f"""
BTC快速分析

当前价格:
${price}

市场状态:
{trend}

建议:
关注关键突破
"""

    except Exception as e:

        return f"分析失败: {e}"