import backtrader
import math

class GoldenCross(backtrader.Strategy):
    params = (('fast', 30),('slow',200),('order_percentage',0.95),("ticker","SPY"))
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.fast_moving_average = backtrader.indicators.SMA(
            self.data.close, period = self.params.fast, plotname = str(self.params.fast)+" days moving average"
        )
        self.slow_moving_average = backtrader.indicators.SMA(
            self.data.close, period = self.params.slow, plotname = str(self.params.slow)+" days moving average"
        )

        self.crossover = backtrader.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average*1.03)
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)

        #print('%s, %s' % (dt.isoformat(), txt))
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
            
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY executed %.2f" % order.executed.price)
                self.price_bought = order.executed.price
            elif order.issell():
                self.log("SELL executed %.2f" % order.executed.price)
        
        self.bar_executed = len(self)
        
        self.order = None

    def next(self):
        if self.position.size ==0:
            if self.crossover>0:
                amount_to_invest = self.params.order_percentage*self.broker.cash
                self.size = math.floor(amount_to_invest / self.data.close)
                self.buy(size = self.size)
                self.log('BUY created, %.2f' % self.dataclose[0])

        if self.position.size >0 :
            if self.crossover <0:
                self.close()
                self.log('SELL created, %.2f' % self.dataclose[0])