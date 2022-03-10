from web3 import Web3

polygonRPC = 'https://polygon-rpc.com/'

web3 = Web3(Web3.HTTPProvider(polygonRPC))

balancerContract = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
balancerABI = [{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"contract IERC20","name":"token","type":"address"}],"name":"getPoolTokenInfo","outputs":[{"internalType":"uint256","name":"cash","type":"uint256"},{"internalType":"uint256","name":"managed","type":"uint256"},{"internalType":"uint256","name":"lastChangeBlock","type":"uint256"},{"internalType":"address","name":"assetManager","type":"address"}],"stateMutability":"view","type":"function"}]
balancer = web3.eth.contract(address=balancerContract, abi=balancerABI)

poolID = "0x2f08387a725c357102cc09b0424d5494dedd52f500020000000000000000036e"
usdcAddress = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
rbwAddress = "0x431CD3C9AC9Fc73644BF68bF5691f4B83F9E104f"

def getRbwBalancerprice():
  usdcBalance = float(web3.fromWei(web3.toWei(balancer.functions.getPoolTokenInfo(poolID,usdcAddress).call()[0],'szabo'),'ether'))
  rbwBalance = float(web3.fromWei(balancer.functions.getPoolTokenInfo(poolID,rbwAddress).call()[0],'ether'))
  price = usdcBalance/rbwBalance
  return(price)