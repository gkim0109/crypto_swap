from crypto_swap.poloniex import *
from crypto_swap.API_Info import *
from Data.dataGenerator import dataGenerator
import time
import decimal

D = decimal.Decimal
myAPI = API_Info()
myPoloniex = poloniex(myAPI.getAPI_Key(), myAPI.getSecret())
coinDict = dict()


def executeTrade():
    tickerDict = myPoloniex.returnTicker()

    btcTickers = {k: v for (k, v) in tickerDict.items() if k.startswith("BTC")}

    #iterlate through coin list in poloniex and identify highest buy signal
    for dict in btcTickers:

        currentPrice = D(tickerDict[dict]['lowestAsk'])
        WMA = D(dataGenerator(dict,time.time()-14400,9999999999,14400).getHistoryChartData()[0]['weightedAverage'])
        buySignal = currentPrice-WMA
        coinDict[dict] =  buySignal

    signalCoin = str(max(coinDict, key=coinDict.get))
    signalCoinIndicator = coinDict[signalCoin]

    print 'Buy signal coin'
    print signalCoin +' SignalIndicator='+ str(signalCoinIndicator)
    print signalCoin
    print type(signalCoin)


    if(signalCoinIndicator>0):
        buyPrice = myPoloniex.returnTicker()[signalCoin]['lowestAsk']
        print 'Purchased ' + signalCoin + 'at a price = ' + str(buyPrice)

        while(True):
            currentPrice = D(myPoloniex.returnTicker()[signalCoin]['lowestAsk'])
            WMA = D(dataGenerator(signalCoin, time.time() - 14400, 9999999999, 14400).getHistoryChartData()[0]['weightedAverage'])
            latestBuySignal = currentPrice - WMA
    
            if(latestBuySignal < signalCoinIndicator  * D('.1')):
                sellPrice = myPoloniex.returnTicker()[signalCoin]['highestBid']
                print 'Sold ' + signalCoin + 'at a price' + str(sellPrice)
                print 'Your return on the trade: ' + str((sellPrice - buyPrice) * 0.92)
                break

print 'Running the paper trading strategy...'
executeTrade()

