from web3 import Web3

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

remainingShadowCornEggs = []
totalLootBox = {
  "rare":0,
  "mythic":0
}
unimLeft = {
  "unim":0
}

def getShadowCorns():
  remainingShadowCornEggs.clear()
  remainingShadowCornEggs.append(darkForest.functions.remainingShadowcornEggs().call())

def getLootBox():
  totalLootBox["rare"] = 0
  totalLootBox["mythic"] = 0
  totalLootBox["rare"] = lootBox.functions.terminusPoolSupply(5).call()
  totalLootBox["mythic"] = lootBox.functions.terminusPoolSupply(6).call()

def getUNIM():
  unimLeft["unim"] = 0
  unimLeft["unim"] = "{:,}".format(int(web3.fromWei(unim.functions.balanceOf('0x8d528e98A69FE27b11bb02Ac264516c4818C3942').call(),'ether')))