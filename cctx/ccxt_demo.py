import ccxt
import json

def get_binance_exchange() :
    binance = ccxt.binance({
        "apiKey": "",
        "secret": "",
    })


    ticker_data = binance.fetch_ticker("BTCUSDT")


    ticker = json.loads(ticker_data)

    print(ticker)




if __name__ == '__main__' :
    get_binance_exchange()

