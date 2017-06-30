from Data.dataGenerator import dataGenerator
from crypto_swap.API_Info import API_Info



def executeBacktest():
    myDataGenerator = dataGenerator('BTC_XMR',1405699200,9999999999,14400)

    for data in myDataGenerator.getHistoryChartData():
        print data

executeBacktest()