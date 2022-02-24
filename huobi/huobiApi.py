import requests
import pandas as pd

pd.set_option("expand_frame_repr", False)

if __name__ == '__main__':
    pass

url = "https://api.huobi.pro/market/history/kline?symbol=btcusdt&period=1day"

resp = requests.get(url)

json = resp.json()["data"]
data = pd.DataFrame(json)


print(data)
