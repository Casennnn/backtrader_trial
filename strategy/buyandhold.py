import backtrader

class BuyandHold(backtrader.Strategy):

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
        
        self.log('BUY created, %.2f' % self.dataclose[0])
        self.order = self.buy(size = self.broker.getvalue()/self.dataclose[0])
        