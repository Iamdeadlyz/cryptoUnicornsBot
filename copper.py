import requests

url = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-polygon-v2"

copperLaunch = """query {
    tokenPrices_1646104700: tokenPrices(
      first: 1
      orderBy: "timestamp"
      orderDirection: "desc"
      where: {poolId: "0x34497b3fd9e337b19f3c0b119cafe78ea7f46a94000200000000000000000323", timestamp_gt: 1646104700, timestamp_lt: 1646348400, asset: "0x431cd3c9ac9fc73644bf68bf5691f4b83f9e104f", pricingAsset: "0x2791bca1f2de4661ed88a30c99a7a9449aa84174"}
    ) {
      price
      timestamp
      __typename
    }
  }
"""

theHeader = {
  "content-type": "application/json"
}

def getRBWCopperPrice():
  data = requests.post(url=url,headers=theHeader,json = {"query":copperLaunch}).json()["data"]["tokenPrices_1646104700"][0]
  return({"price":data["price"],"timeAndDate":data["timestamp"]})