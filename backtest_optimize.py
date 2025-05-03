import backtrader
import datetime
import os
import time
import math
from strategy.buyandhold import BuyandHold
from strategy.goldencross import GoldenCross
from tqdm import tqdm
import pandas as pd
import yfinance as yf

sp500_sample = [
    'AMZN','META','NVDA','GOOG','JPM','TSLA','MSFT','AAPL','GOOGL','LLY','AVGO','WMT','XOM','UNH','MA','PG','ORCL','COST','JNJ','HD','MRK','BAC','ABBV','NFLX','CVX','AMD','CRM','ADBE','PEP','QCOM','TMO','LIN','WFC','TMUS','ACN','AMAT','CSCO','DHR','MCD','INTU','DIS','ABT','TXN','GE','VZ','AMGN','AXP','CAT','NOW','IBM','PFE','MS','ISRG','PM','CMCSA','UBER','BX','GS','MU','NEE','SPGI','LRCX','HON','UNP','T','BKNG','RTX','COP','INTC','SCHW','SYK','ELV','LOW','ETN','TJX','PGR','C','VRTX','UPS','BLK','REGN','NKE','ADI','BSX','LMT','BA','KLAC','ANET','PANW','MMC','PLD','CB','DE','MDT','ADP','ABNB','CI','SNPS','AMT','SBUX','MDLZ','FI','CMG','WM','GILD','SO','BMY','HCA','CDNS','APH','CL','GD','ZTS','ICE','MO','DUK','MCO','MCK','SHW','TT','CVS','FDX','EOG','EQIX','TDG','CTAS','CME','ITW','FCX','MAR','NXPI','TGT','ECL','BDX','SLB','CSX','PH','NOC','MSI','AON','CEG','EMR','WELL','ORLY','USB','PNC','RSG','MPC','PYPL','ROP','PSX','APD','CARR','AJG','MMM','OXY','EW','HLT','PCAR','ADSK','GM','COF','CPRT','MNST','TFC','WMB','VLO','AFL','AZO','PSA','MET','SPG','AIG','F','MCHP','DLR','NSC','ROST','NEM','SRE','SMCI','OKE','STZ','TRV','KMB','DHI','AEP','TEL','FTNT','O','MRNA','HES','KDP','DXCM','HUM','COR','BK','JCI','GWW','KMI','URI','CHTR','PAYX','LHX','CCI','AMP','ALL','PRU','FIS','LEN','D','RCL','IDXX','MPWR','KHC','OTIS','AME','IQV'
]

#input area
strategyToBeTested = GoldenCross
periodd = 5
testnum = int(input("Enter the number of stocks to be tested...(1 to 218) "))

stockToPlot = 'AMZN'
rangeoflongtermSMA = [200, 300]
rangeofshorttermSMA = [20,30]   #range(10,110,10)
#input end



#----this is the stock's return----
basedictt = {}
for stockname in tqdm(sp500_sample):
    if len(basedictt) >= testnum:  #just to stop at testnum case
        break
    stock = yf.Ticker(stockname)
    cerebro = backtrader.Cerebro()
    cerebro.broker.set_cash(10000)
    cerebro.addstrategy(BuyandHold)
    data = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y'), name = stockname)
    cerebro.adddata(data)
    try:
        startingValue = cerebro.broker.getvalue()
        cerebro.run()
        #cerebro.plot()
        endingValue = cerebro.broker.getvalue() 
        annualreturn = (endingValue/startingValue) ** (1/int(periodd)) -1
        basedictt[stockname]=round(annualreturn,4)
    except:
        continue

basesumOfReturn =0
basewinCount =0
for i in basedictt.values():
    basesumOfReturn+=i
    if i>0:
        basewinCount+=1




#----this is the strategy's return----

for daysell in rangeoflongtermSMA:
    for testVar in rangeofshorttermSMA:
        dict_name = f"returnDict{testVar}and{daysell}"
        globals()[dict_name] = {}
        for stockname in tqdm(sp500_sample):
            if len(globals()[dict_name]) >= testnum:  #just to stop at testnum case
                break
            stock = yf.Ticker(stockname)
            cerebro = backtrader.Cerebro()
            cerebro.broker.set_cash(10000)
            cerebro.addstrategy(strategyToBeTested,fast=testVar, slow=daysell)
            data = backtrader.feeds.PandasData(dataname = stock.history(period=str(periodd)+'y'), name = stockname)
            cerebro.adddata(data)
            
            startingValue = cerebro.broker.getvalue()
            cerebro.run()
            if stockname == stockToPlot:
                cerebro.plot(style='candle')
            endingValue = cerebro.broker.getvalue() 
            annualreturn = (endingValue/startingValue) ** (1/int(periodd)) -1
            globals()[dict_name][stockname]=round(annualreturn,4)
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
# diff = {k: round(returnDict[k] - basedictt[k],4 )for k in returnDict.keys()}

# sorted_dict = dict(sorted(diff.items(), key=lambda x: x[1], reverse=True))
# print(sorted_dict) #dict of the diff

print("\nFOR THE STOCKS:")
print("\nAverage annual return is ",round(basesumOfReturn/len(basedictt),6))
print("Number of Wins is ", basewinCount)
print("Number of Losses is ", len(basedictt)-basewinCount)
print('\n')



for daysell in rangeoflongtermSMA:
    print("\n***** Long SMA ", daysell, " ******")
    for testVar in rangeofshorttermSMA:
        dict_name = f"returnDict{testVar}and{daysell}"
        sumOfReturn =0
        for value in globals()[dict_name].values():
            sumOfReturn+=value
        averageReturn = sumOfReturn/len(globals()[dict_name])
        print("Using ",testVar," days Short Moving average: ", round(averageReturn,6))



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

# print("\naverage excess return is ",round(benchmarkSum/len(returnDict),6))
# print("Number of beating the stock is ", benchmarkWinCount)
# print("Number of Losses is ", len(returnDict)-benchmarkWinCount)
wait = input("Program ends...")