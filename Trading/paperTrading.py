from crypto_swap.poloniex import *
from crypto_swap.API_Info import *
from Data.dataGenerator import dataGenerator
import time
import decimal
from SmsNotification.txtTest import twilioAPI

D = decimal.Decimal
myAPI = API_Info()
myPoloniex = poloniex(myAPI.getAPI_Key(), myAPI.getSecret())
coinDict = dict()
profitList = []
myTwilioAPI = twilioAPI('')

def executeTrade():
    tickerDict = myPoloniex.returnTicker()

    btcTickers = {k: v for (k, v) in tickerDict.items() if k.startswith("BTC")}

    #iterlate through coin list in poloniex and identify highest buy signal
    for dict in btcTickers:
        currentPrice = D(tickerDict[dict]['lowestAsk'])
        # Use a fiv minute period divisions
        WMA = D(dataGenerator(dict,time.time()-300,9999999999,300).getHistoryChartData()[0]['weightedAverage'])
        if(WMA != 0):
            buySignal = D(currentPrice-WMA)/D(currentPrice)
            coinDict[dict] =  buySignal

    signalCoin = str(min(coinDict, key=coinDict.get))
    signalCoinIndicator = coinDict[signalCoin]

    print 'Buy signal coin'
    print signalCoin +' SignalIndicator='+ str(signalCoinIndicator)

    treshHold = -0.02
    if(signalCoinIndicator<treshHold):
        buyPrice = myPoloniex.returnTicker()[signalCoin]['lowestAsk']
        buyPrice = D(buyPrice)
        print 'Purchased ' + signalCoin + 'at a price = ' + str(buyPrice)

        while(True):
            currentPrice = D(myPoloniex.returnTicker()[signalCoin]['lowestAsk'])
            WMA = D(dataGenerator(signalCoin, time.time() - 300, 9999999999, 300).getHistoryChartData()[0]['weightedAverage'])
            latestBuySignal = D(currentPrice-WMA)/D(currentPrice)

            if(latestBuySignal > signalCoinIndicator  * D('0.025')):
                sellPrice = myPoloniex.returnTicker()[signalCoin]['highestBid']
                sellPrice = D(sellPrice)
                print 'Sold ' + signalCoin + 'at a price' + str(sellPrice)

                siippage = D('0.08')

                tradereturn = sellPrice - buyPrice
                profit = (tradereturn) - (tradereturn) * siippage
                print 'Your return on the trade: ' + str(profit)
                profitList.append(profit)
                break
    else:
        profitList.append(D('0.0'))


print 'Running the paper trading strategy...'
for i in range(0,25):
    executeTrade()

profitMessage = 'Total Profit: ' + str(sum(profitList))
print profitMessage

myTwilioAPI.setMessage(profitMessage)
myTwilioAPI.sendMessage()
