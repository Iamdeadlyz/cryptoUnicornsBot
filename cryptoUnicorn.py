from web3 import Web3
import requests
import json
import time

polygonRPC = 'https://polygon-rpc.com/'

web3 = Web3(Web3.HTTPProvider(polygonRPC))

darkForestContract = '0x8d528e98A69FE27b11bb02Ac264516c4818C3942'
darkForestABI = '[{"inputs":[],"name":"remainingShadowcornEggs","outputs":[{"internalType":"uint256[3]","name":"","type":"uint256[3]"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
darkForest = web3.eth.contract(address=darkForestContract, abi=darkForestABI)

lootBoxContract = '0x99A558BDBdE247C2B2716f0D4cFb0E246DFB697D'
lootBoxABI = '[{"inputs":[{"internalType":"uint256","name":"poolID","type":"uint256"}],"name":"terminusPoolSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
lootBox = web3.eth.contract(address=lootBoxContract, abi=lootBoxABI)

unimContract = '0x64060aB139Feaae7f06Ca4E63189D86aDEb51691'
unimABI = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
unim = web3.eth.contract(address=unimContract, abi=unimABI)

def getShadowCorns():
  return(darkForest.functions.remainingShadowcornEggs().call())

def getLootBox():
  totalLootBox = {
    "rare":0,
    "mythic":0
  }
  totalLootBox["rare"] = 0
  totalLootBox["mythic"] = 0
  totalLootBox["rare"] = lootBox.functions.terminusPoolSupply(5).call()
  totalLootBox["mythic"] = lootBox.functions.terminusPoolSupply(6).call()
  return(totalLootBox)

def getUNIM():
  unimLeft = {
    "unim":0
  }
  unimLeft["unim"] = "{:,}".format(int(web3.fromWei(unim.functions.balanceOf('0x8d528e98A69FE27b11bb02Ac264516c4818C3942').call(),'ether')))
  return(unimLeft)


#####################################################################
#Polygonscan data
#Get here https://polygonscan.com/myapikey

polygonScanAPIKey = "apiKeyGoesHere"

def getBlockNumber():
  with open('summonTransactions.json', 'r') as tx:
    theTx = json.load(tx)
  transactions = len(theTx) - 1
  return (int(theTx[transactions]["blockNumber"]))

def updateTransactions():
  past = getBlockNumber()
  transactions = requests.get(f"https://api.polygonscan.com/api?module=account&action=txlist&address=0x8d528e98A69FE27b11bb02Ac264516c4818C3942&startblock={past}&endblock=99999999&page=1&offset=9000&sort=asc&apikey={polygonScanAPIKey}").json()["result"]
  if len(transactions) > 0:
    with open('summonTransactions.json', 'r') as tx:
      theTx = json.load(tx)
    alreadyExists = []
    for existing in theTx:
      alreadyExists.append(existing["hash"])
    for tx in transactions:
      if tx['hash'] not in alreadyExists and tx['isError'] == "0" and ("0xe8399812" in tx['input'] or "0x54a81405" in tx['input']): #filter successful tx only and get sacrifice related tx
        theTx.append(tx)
    with open('summonTransactions.json', 'w') as saveTx:
      json.dump(theTx,saveTx)
    time.sleep(1)
    if past != getBlockNumber():
      updateTransactions()

def getRequestIDs():
  with open('summonTransactions.json', 'r') as tx:
    theTx = json.load(tx)
  for tx in theTx:
    if "0xe8399812" in tx['input'] and tx.get("requestID") is None: #For offer sacrifice
      txhash = tx['hash']
      tx["requestID"] = web3.eth.get_transaction_receipt(txhash)["logs"][5]["data"][-64:]
    elif "0x54a81405" in tx['input'] and tx.get("requestID") is None: #For sacrifice completed
      txhash = tx['hash']
      tx["requestID"] = web3.eth.get_transaction_receipt(txhash)["logs"][1]["data"][-64:]
      tx["reward"] = web3.toInt(web3.eth.get_transaction_receipt(txhash)["logs"][1]["topics"][2])
  with open('summonTransactions.json','w') as theFile:
    json.dump(theTx,theFile)

def filterSummons():
  summons = {
    "basic":{
      "totalSummon":0,
      "lootbox":{
        "rare":0
      },
      "shadowCorns":{
        "common":0,
        "rare":0,
        "mythic":0
      }
    },
    "complex":{
      "totalSummon":0,
      "lootbox":{
        "mythic":0
      },
      "shadowCorns":{
        "common":0,
        "rare":0,
        "mythic":0
      }
    },
    "advanced":{
      "totalSummon":0,
      "shadowCorns":{
        "common":0,
        "rare":0,
        "mythic":0
      }
    },
    "overall":{
      "totalShadowCorns":0,
      "common":0,
      "rare":0,
      "mythic":0
    }
  }
  itemIDs1= {
    1:"shadowCorns",
    2:"shadowCorns",
    3:"shadowCorns",
    5:"lootbox",
    6:"lootbox"
  }
  itemIDs2 = {
    1:"common",
    2:"rare",
    3:"mythic",
    5:"rare",
    6:"mythic"
  }
  with open('summonTransactions.json', 'r') as tx:
    theTx = json.load(tx)
  for x in range(len(theTx)):
    if "0xe8399812" in theTx[x]['input']:
      for y in range(len(theTx)):
        if "0x54a81405" in theTx[y]['input'] and (theTx[x]["requestID"] == theTx[y]["requestID"]):
          if "0xe8399812" in theTx[x]['input'] and "10f0cf064dd59200000" in theTx[x]['input']:
            summons["basic"]["totalSummon"] += 1
            summons["basic"][itemIDs1.get(theTx[y]['reward'])][itemIDs2.get(theTx[y]['reward'])] += 1
          elif "0xe8399812" in theTx[x]['input'] and "472698b413b43200000" in theTx[x]['input']:
            summons["complex"]["totalSummon"] += 1
            summons["complex"][itemIDs1.get(theTx[y]['reward'])][itemIDs2.get(theTx[y]['reward'])] += 1
          elif "0xe8399812" in theTx[x]['input'] and "73324c9144791400000" in theTx[x]['input']:
            summons["advanced"]["totalSummon"] += 1
            summons["advanced"][itemIDs1.get(theTx[y]['reward'])][itemIDs2.get(theTx[y]['reward'])] += 1
  summons["overall"]["totalShadowCorns"] = summons["basic"]["shadowCorns"]["common"] + summons["basic"]["shadowCorns"]["rare"] + summons["basic"]["shadowCorns"]["mythic"] + summons["complex"]["shadowCorns"]["common"] + summons["complex"]["shadowCorns"]["rare"] + summons["complex"]["shadowCorns"]["mythic"] + summons["advanced"]["totalSummon"]
  summons["overall"]["common"] = summons["basic"]["shadowCorns"]["common"] + summons["complex"]["shadowCorns"]["common"] + summons["advanced"]["shadowCorns"]["common"]
  summons["overall"]["rare"] = summons["basic"]["shadowCorns"]["rare"] + summons["complex"]["shadowCorns"]["rare"] + summons["advanced"]["shadowCorns"]["rare"]
  summons["overall"]["mythic"] = summons["basic"]["shadowCorns"]["mythic"] + summons["complex"]["shadowCorns"]["mythic"] + summons["advanced"]["shadowCorns"]["mythic"]
  return(summons)