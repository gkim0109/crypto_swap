from crypto_swap.poloniex import *
from crypto_swap.API_Info import *
import csv

class dataGenerator():

    def __init__(self, currencyPair, start, end, period):
        self.currencyPair = currencyPair
        self.start = start
        self.end = end
        self.period = period
        self.apiInfo = API_Info()
        self.poloniexClass = poloniex(self.apiInfo.getAPI_Key(), self.apiInfo.getSecret())

    def setCurrnecyPair(self, currencyPair):
        self.currencyPair = currencyPair

    def setStartTime(self, start):
        self.start = start

    def setEndTime(self, end):
        self.end = end

    def setPeriod(self, period):
        self.period = period


    def generateHistoryChartCSV(self):

        json_list = self.poloniexClass.api_query("returnChartData", {"currencyPair" : self.currencyPair}, self.period,self.start, self.end)

        print("length of the list: " + str(len(json_list)))

        with open("sample.csv", "wb") as csvfile:
            fieldNames= ["volume","quoteVolume", "high", "low", "date","close", "weightedAverage", "open"]

            writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
            writer.writeheader()
            for item in json_list:
                writer.writerow(item)

        csvfile.close()

    def getHistoryChartData(self):

        json_list = self.poloniexClass.api_query("returnChartData", {"currencyPair": self.currencyPair}, self.period,
                                            self.start, self.end)
        while(json_list == "error"):
            json_list = self.poloniexClass.api_query("returnChartData", {"currencyPair": self.currencyPair}, self.period,
                                            self.start, self.end)
        return json_list

