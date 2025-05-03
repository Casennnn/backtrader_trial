import backtrader

class MyStrategy(backtrader.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)

        #print('%s, %s' % (dt.isoformat(), txt))
    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

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
        self.log("Closing at %.2f" % self.dataclose[0])

        if self.order:
            return #already have an order pending

        #if not self.position:
        if self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1]<self.dataclose[-2]:
            self.log('BUY created, %.2f' % self.dataclose[0])
            self.order = self.buy(size = self.broker.getvalue()/self.dataclose[0]/5)
        if self.position:
            #sell
            self.log("Price being compared is %.2f" % self.price_bought)
            # print('\n')
            # self.log(self.position)
            if len(self)>=(self.bar_executed +2) and self.dataclose[0]>=self.price_bought:
                self.log('SELL created, %.2f' % self.dataclose[0])
                self.order = self.sell(size = self.position.size)
            elif len(self)>=(self.bar_executed +2) and self.dataclose[0]<=self.price_bought*0.9:
            #stop loss of 10%
                self.log('SELL created, %.2f' % self.dataclose[0])
                self.log('STOPLOSS')
                self.order = self.sell(size = self.position.size)
                # problem is selling everything if the price is higher than the last bought price, need cal the avg price
        
         