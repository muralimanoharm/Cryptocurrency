# importing the requests library 
import requests
import json
import inspect, re

def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
         return m.group(1)

class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 

def GetBitbnsData():
    # api-endpoint 
    bitbnsURL = "https://bitbns.com/order/getTickerWithVolume/"
    bitbnsres = requests.get(url = bitbnsURL)
    # extracting data in json format 
    bitbnsdata = bitbnsres.json()
    return bitbnsdata

def GetWazirxData():
    # api-endpoint 
    wazirxURL =  "https://api.wazirx.com/api/v2/market-status"
    wazirxres = requests.get(url = wazirxURL)
    # extracting data in json format 
    wazirxdata = wazirxres.json()
    return wazirxdata

def CompareBitbnsAndWazrixData():
    coins=[]
    bitbnsdata = GetBitbnsData()
    wazirxdata = GetWazirxData()
    bitbnsDict = my_dictionary()
    wazirxDict =my_dictionary()
    for key in bitbnsdata:
        coins.append(key.upper())
        bitbnsDict.add(key.upper() , bitbnsdata[key]["last_traded_price"])
        
    for key in wazirxdata['markets']:
        if key['quoteMarket']=='inr':
            wazirxDict.add(key['baseMarket'].upper(),key['last'])
    return coins,bitbnsDict,wazirxDict
    

def CompareThePriceInTwoExchanges(coin,bitbns,wazirx):
    if coin in bitbns and coin in wazirx:    
        #print(coin," Price Comparison :",bitbns[coin]," :",wazirx[coin])
        max = bitbns[coin]
        maxexchange ="bitbns"
        low = wazirx[coin]
        lowexchange ="wazirx"
        if(float(bitbns[coin]) < float(wazirx[coin])):
            max = wazirx[coin]
            maxexchange ="wazirx"
            low = bitbns[coin]
            lowexchange ="bitbns"
        #Get The margin for 10000 Rupees
        #find the acquirable coin for 10000 rupees
        amountAvailable = 10000
        acquirableCoins = amountAvailable / float(low)
        profit = (acquirableCoins* float(max)) - amountAvailable          
        print("Buy ",coin," from",lowexchange,"at ",low," you get ",acquirableCoins," and sell at ",maxexchange," at ",max," to get ",profit)
        
coins,bitbnsDict,wazirxDict = CompareBitbnsAndWazrixData()
for coin in coins:
    CompareThePriceInTwoExchanges(coin,bitbnsDict,wazirxDict)


