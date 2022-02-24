import requests

if __name__ == '__main__':
    pass



url = "https://api.huobi.pro/v2/settings/common/currencies"


resp = requests.get(url)

print(resp)





