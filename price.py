import requests
from datetime import datetime, timedelta

unimPrice = "https://api.coingecko.com/api/v3/simple/price?ids=unicorn-milk&vs_currencies=eth,usd,php,cad,zar,huf,cny,rub,thb"

coinGeckoHeader = {
  "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

priceOfUNIM = {
  "eth":0,
  "usd":0,
  "php":0,
  "cad":0,
  "zar":0,
  "huf":0,
  "cny":0,
  "rub":0,
  "thb":0
}

#For simple caching. Value for default purpose.
currentTime = {
  "time":"2022-02-13 04:02:31.042211"
}

def getUNIMPrice():
  #Caching data every 30s
  savedTime = datetime.strptime(currentTime["time"],"%Y-%m-%d %H:%M:%S.%f")
  if (datetime.now()-savedTime) > timedelta(seconds=30):
    price = requests.get(unimPrice,headers=coinGeckoHeader).json()["unicorn-milk"]
    priceOfUNIM["eth"] = price["eth"]
    priceOfUNIM["usd"] = price["usd"]
    priceOfUNIM["php"] = price["php"]
    priceOfUNIM["cad"] = price["cad"]
    priceOfUNIM["zar"] = price["zar"]
    priceOfUNIM["huf"] = price["huf"]
    priceOfUNIM["cny"] = price["cny"]
    priceOfUNIM["rub"] = price["rub"]
    priceOfUNIM["thb"] = price["thb"]
    currentTime["time"] = str(datetime.now())
  else:
    pass