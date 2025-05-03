import backtrader
import datetime
import os
import time
import math
from strategy.multidataframe import SpotGreatTrend, UptrendObserver
from strategy.buyandhold import BuyandHold
from strategy.goldencross import GoldenCross
from tqdm import tqdm
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


# sp500 = [
#     'BTC-USD','AMZN','META','NVDA','GOOG','JPM','TSLA','MSFT','AAPL','GOOGL','LLY','AVGO','WMT','XOM','UNH','MA','PG','ORCL','COST','JNJ','HD','MRK','BAC','ABBV','NFLX','CVX','AMD','CRM','ADBE','PEP','QCOM','TMO','LIN','WFC','TMUS','ACN','AMAT','CSCO','DHR','MCD','INTU','DIS','ABT','TXN','GE','VZ','AMGN','AXP','CAT','NOW','IBM','PFE','MS','ISRG','PM','CMCSA','UBER','BX','GS','MU','NEE','SPGI','LRCX','HON','UNP','T','BKNG','RTX','COP','INTC','SCHW','SYK','ELV','LOW','ETN','TJX','PGR','C','VRTX','UPS','BLK','REGN','NKE','ADI','BSX','LMT','BA','KLAC','ANET','PANW','MMC','PLD','CB','DE','MDT','ADP','ABNB','CI','SNPS','AMT','SBUX','MDLZ','FI','CMG','WM','GILD','SO','BMY','HCA','CDNS','APH','CL','GD','ZTS','ICE','MO','DUK','MCO','MCK','SHW','TT','CVS','FDX','EOG','EQIX','TDG','CTAS','CME','ITW','FCX','MAR','NXPI','TGT','ECL','BDX','SLB','CSX','PH','NOC','MSI','AON','CEG','EMR','WELL','ORLY','USB','PNC','RSG','MPC','PYPL','ROP','PSX','APD','CARR','AJG','MMM','OXY','EW','HLT','PCAR','ADSK','GM','COF','CPRT','MNST','TFC','WMB','VLO','AFL','AZO','PSA','MET','SPG','AIG','F','MCHP','DLR','NSC','ROST','NEM','SRE','SMCI','OKE','STZ','TRV','KMB','DHI','AEP','TEL','FTNT','O','MRNA','HES','KDP','DXCM','HUM','COR','BK','JCI','GWW','KMI','URI','CHTR','PAYX','LHX','CCI','AMP','ALL','PRU','FIS','LEN','D','RCL','IDXX','MPWR','KHC','OTIS','AME','IQV'
# ]
# market_caps = []
# for ticker in sp500:
#     try:
#         stock = yf.Ticker(ticker)
#         market_cap = stock.info['marketCap']
#         market_caps.append((ticker, market_cap))
#     except:
#         pass

# market_caps.sort(key=lambda x: x[1], reverse=True)
# sp500_sample = [ticker for ticker, _ in market_caps[:100]]
sp500_sample = ['AMZN','AAPL','JPM', 'MSFT',  'GOOG', 'GOOGL',  'META', 'TSLA', 'LLY', 'AVGO', 'JPM', 'WMT', 'XOM', 'UNH', 'MA', 'PG', 'ORCL', 'JNJ', 'COST', 'HD', 'BAC', 'MRK', 'ABBV', 'CVX', 'NFLX', 'AMD', 'ADBE', 'CRM', 'PEP', 'LIN', 'TMUS', 'QCOM', 'TMO', 'ACN', 'WFC', 'CSCO', 'TXN', 'MCD', 'DHR', 'AMAT', 'AXP', 'INTU', 'AMGN', 'VZ', 'DIS', 'CAT', 'ABT', 'GE', 'IBM', 'MS', 'PFE', 'PM', 'BX', 'CMCSA', 'GS', 'NOW', 'SPGI', 'INTC', 'UNP', 'ISRG', 'NEE', 'HON', 'UBER', 'RTX', 'T', 'LOW', 'COP', 'BKNG', 'PGR', 'MU', 'TJX', 'SYK', 'VRTX', 'C', 'LRCX', 'UPS', 'ETN', 'BLK', 'ADI', 'REGN', 'ELV', 'SCHW', 'PLD', 'LMT', 'BSX', 'BA', 'NKE', 'CB', 'MMC', 'KLAC', 'DE', 'PANW', 'ANET', 'MDT', 'ADP', 'AMT', 'CI', 'ABNB', 'FI', 'GILD']

#input area
strategyToBeTested = SpotGreatTrend
periodd = 10
testnum = int(input("Enter the number of stock that want to be tested. "))
stockToPlot = 'AMZN'
rangeofAF = range(5, 50, 2)
#input end
listtostorecount = []




#----this is the stock's return----
# basedictt = {}
# for stockname in tqdm(sp500_sample):
#     if len(basedictt) >= testnum:  #just to stop at testnum case
#         break
#     stock = yf.Ticker(stockname)
#     cerebro = backtrader.Cerebro()
#     cerebro.broker.set_cash(10000)
#     cerebro.addstrategy(GoldenCross)
#     data = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y', interval = '1wk'), name = stockname)
#     cerebro.adddata(data)
#     try:
#         startingValue = cerebro.broker.getvalue()
#         cerebro.run()
#         cerebro.plot()
#         endingValue = cerebro.broker.getvalue() 
#         annualreturn = (endingValue/startingValue) ** (1/int(periodd)) -1
#         basedictt[stockname]=round(annualreturn,4)
#     except:
#         continue

# basesumOfReturn =0
# basewinCount =0
# for i in basedictt.values():
#     basesumOfReturn+=i
#     if i>0:
#         basewinCount+=1


#----this is the strategy's return----




for i in tqdm(rangeofAF):
    testVar = 0.0001*i
    dict_name = f"returnDictAF{testVar}"
    globals()[dict_name] = {}
    for stockname in sp500_sample:
        if len(globals()[dict_name]) >= testnum:  #just to stop at testnum case
            break
        stock = yf.Ticker(stockname)
        cerebro = backtrader.Cerebro(stdstats=False)
        cerebro.broker.set_cash(10000)
        cerebro.addstrategy(strategyToBeTested, afparam = testVar)
        # cerebro.addobserver(backtrader.observers.Trades)
        # cerebro.addobserver(backtrader.observers.Benchmark)
        dailydata = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y', interval = "1d"), name = stockname)
        weeklydata = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y', interval = "1wk"), name = stockname)
        cerebro.adddata(dailydata)
        cerebro.adddata(weeklydata)
        startingValue = cerebro.broker.getvalue()
        cerebro.addobserver(backtrader.observers.Broker)
        cerebro.addobserver(backtrader.observers.BuySell)
        results = cerebro.run()
        numoftrade = results[0].output_value()
        # if stockname == stockToPlot:
            # cerebro.plot(style="candle")
        endingValue = cerebro.broker.getvalue() 
        annualreturn = (endingValue/startingValue) ** (1/int(periodd)) -1
        globals()[dict_name][stockname]=[round(annualreturn,4),numoftrade]

        # except:
        #     print('error')
        #     continue

# sumOfReturn =0
# winCount =0
# for i in returnDict.values():
#     sumOfReturn+=i
#     if i>0:
#         winCount+=1

#print strat - base
# diff = {k: round(returnDict[k] - basedictt[k],4 )for k in returnDict30soldin45.keys()}

# sorted_dict30soldin45 = dict(sorted(returnDict30soldin45.items(), key=lambda x: x[1], reverse=True))
#sorted_dict30soldin360 = dict(sorted(returnDict30soldin360.items(), key=lambda x: x[1], reverse=True))


# beststock1 = list(returnDict.keys())[0]
# #beststock2 = list(sorted_dict30soldin360.keys())[0]

# worststock1 = list(returnDict.keys())[-1]
#worststock2 = list(sorted_dict30soldin360.keys())[-1]







# print("\nFOR THE STOCKS:")
# print("\nAverage annual return is ",round(basesumOfReturn/len(basedictt)*100,6), "%")
# print("Number of Wins is ", basewinCount)
# print("Number of Losses is ", len(basedictt)-basewinCount)
# print('\n')





# startdate = datetime.datetime.now()- datetime.timedelta(days=5)
# rf = yf.Ticker("^IRX").history(start=startdate)

x = [round(0.001 * (i+1), 4) for i in rangeofAF]
stopcount = 0
for stockname in sp500_sample:
    if stopcount >= testnum:
        break
    stopcount += 1
    # print("\nFOR ",stockname, ":")
    list_name = f"listofReturn{stockname}"
    globals()[list_name] = []
    for i in rangeofAF:
        testVar = i*0.0001
        # print("With AF = ", round(testVar,4))
        
        dict_name = f"returnDictAF{testVar}"
        # print("Return = ", round(globals()[dict_name][stockname][0]*100,4), "% , Num of trades = ",globals()[dict_name][stockname][1] )
        # print("===========")
        globals()[list_name].append(globals()[dict_name][stockname][0]*100)
        
    
    plt.plot(x, globals()[list_name] , label = stockname)



plt.legend()
plt.xlabel('AF')
plt.ylabel('Return (%)')
plt.show()


# print("\nFOR YOUR STRATEGY:")
# print("\nAverage annual return is ",round(sumOfReturn/len(basedictt),6))
# print("Number of Wins is ", winCount)
# print("Number of Losses is ", len(returnDict)-winCount)

# benchmarkWinCount =0
# benchmarkSum = 0
# for i in diff:
#     benchmarkSum += diff[i]
#     if diff[i]>0:
#         benchmarkWinCount +=1

# print("\naverage excess return is ",round(benchmarkSum/len(returnDict30soldin45)*100,6), "%")
# print("Number of beating the stock is ", benchmarkWinCount)
# print("Number of Losses is ", len(returnDict30soldin45)-benchmarkWinCount)


# listofstocktoplot = [beststock1, worststock1]

# print("\n")
# print("Stock with highest return: ", beststock1)
# #print("best stock from 30 moving average, sell in 360 days is: ", beststock2)
# print("Stock with lowest return: ", worststock1)
#print("worst stock from 30 moving average, sell in 360 days is: ", worststock2)



        
# stock = yf.Ticker(beststock1)
# cerebro = backtrader.Cerebro()
# cerebro.broker.set_cash(10000)
# cerebro.addstrategy(strategyToBeTested,fastparam=30, daytosell=45)
# data = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y'), name = stockname)
# cerebro.adddata(data)
# cerebro.run()
# cerebro.plot()

# stock = yf.Ticker(beststock2)
# cerebro = backtrader.Cerebro()
# cerebro.broker.set_cash(10000)
# cerebro.addstrategy(strategyToBeTested,fastparam=30, daytosell=360)
# data = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y'), name = stockname)
# cerebro.adddata(data)
# cerebro.run()
# cerebro.plot()

# stock = yf.Ticker(worststock1)
# cerebro = backtrader.Cerebro()
# cerebro.broker.set_cash(10000)
# cerebro.addstrategy(strategyToBeTested,fastparam=30, daytosell=45)
# data = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y'), name = stockname)
# cerebro.adddata(data)
# cerebro.run()
# cerebro.plot()

# stock = yf.Ticker(worststock2)
# cerebro = backtrader.Cerebro()
# cerebro.broker.set_cash(10000)
# cerebro.addstrategy(strategyToBeTested,fastparam=30, daytosell=360)
# data = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y'), name = stockname)
# cerebro.adddata(data)
# cerebro.run()
# cerebro.plot()
best_return = None
best_stock = None
best_af = None

for i in tqdm(rangeofAF):
    dict_name = f"returnDictAF{0.0001 * i}"
    if dict_name in globals():
        returns_dict = globals()[dict_name]
        if returns_dict:  # Check if the dictionary is not empty
            for stockname, values in returns_dict.items():
                annual_return = values[0]  # Extract the annual return
                if best_return is None or annual_return > best_return:
                    best_return = annual_return
                    best_stock = stockname
                    best_af = 0.0001 * i


print("The best stock is ", best_stock, " with acceleration factor of ", best_af)


stock = yf.Ticker(best_stock)
cerebro = backtrader.Cerebro(stdstats=False)
cerebro.broker.set_cash(10000)
cerebro.addstrategy(strategyToBeTested, afparam = best_af)
# cerebro.addobserver(backtrader.observers.Trades)
# cerebro.addobserver(backtrader.observers.Benchmark)
dailydata = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y', interval = "1d"), name = stockname)
weeklydata = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y', interval = "1wk"), name = stockname)
cerebro.adddata(dailydata)
cerebro.adddata(weeklydata)
startingValue = cerebro.broker.getvalue()
cerebro.addobserver(backtrader.observers.Broker)
cerebro.addobserver(backtrader.observers.BuySell)
results = cerebro.run()
numoftrade = results[0].output_value()

cerebro.plot(style="candle")




wait = input("Program ends.")

