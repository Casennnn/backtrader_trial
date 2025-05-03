import backtrader
import math


class UptrendObserver(backtrader.Observer):
    lines = ('uptrend','SARbull')
    plotinfo = dict(plot=True, subplot=True, plotname='Uptrend')

    def next(self):
        self.lines.uptrend[0] = self._owner.onUptrend
        self.lines.SARbull[0] = self._owner.SARbull




class SpotGreatTrend(backtrader.Strategy):
    params = (('fast', 20),('slow',30))
    def __init__(self, afparam=10):
        self.order = None
        self.countrade = 0
        self.fast_moving_average = backtrader.indicators.EMA(
            self.datas[1].close, period = self.params.fast, plotname = str(self.params.fast)+" weeks EMA"
        )
        self.slow_moving_average = backtrader.indicators.EMA(
            self.datas[1].close, period = self.params.slow, plotname = str(self.params.slow)+" weeks EMA"
        )
        self.SAR = backtrader.indicators.ParabolicSAR(
            self.datas[1], period = 2, af = afparam, afmax=0.2
        )
        self.onUptrend = 0
        self.uptrend_observer = UptrendObserver()
        self.SARbull = 0
        self.trades = []

        # self.crossover = backtrader.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average*1.02, plotname="buycross_enter")
        # self.crossover_exit = backtrader.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average, plotname="buycross_exit")
        # self.crossover_short = backtrader.indicators.CrossOver(self.slow_moving_average, self.fast_moving_average*1.02, plotname = "shortcross_enter")
        # self.crossover_short_exit = backtrader.indicators.CrossOver(self.slow_moving_average, self.fast_moving_average, plotname = "shortcross_exit")

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
            
        if order.status in [order.Completed]:
            # if order.exectype == backtrader.Order.Stop:
            #     print("SAR Trailing stop", self.data._name)

            if order.isbuy():
                self.log("BUY executed %.2f" % order.executed.price)
                self.price_bought = order.executed.price
            elif order.issell():
                self.log("SELL executed %.2f" % order.executed.price)
        
        self.bar_executed = len(self)
        
        self.order = None

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trades.append(trade)
            self.current_trade = None
        elif trade.isopen:
            self.current_trade = trade



    def next(self):
        if self.datas[0].datetime.date(0) == self.datas[0].datetime.date(-1):
            return
        self.log("Close at %.2f" %self.datas[0].close[0])
        # self made indicator on general trend:
        if self.onUptrend ==0:
            if self.fast_moving_average[0]>self.slow_moving_average[0]*1.02 and self.fast_moving_average[0]>self.fast_moving_average[-1] and self.slow_moving_average[0]>self.slow_moving_average[-1]:
                self.onUptrend = 1 
        if self.onUptrend ==1:
            if self.fast_moving_average[0]<= self.slow_moving_average[0]:
                self.onUptrend = 0
        # self made indicator on small trend using PSAR:
        if self.SAR[0] > self.datas[0].close[0]:
            self.SARbull = -1
        elif self.SAR[0] < self.datas[0].close[0]:
            self.SARbull = 1
        


        
        if self.order == None:
            if self.position.size ==0:
                if self.onUptrend>0:
                    if self.SARbull>0:
                        amount_to_invest = self.broker.cash
                        self.size = math.floor(amount_to_invest / self.data.close)
                        self.order = self.buy(size = self.size)
                        self.countrade +=1
                        self.log('BUY created, %.2f' % self.datas[0].close[0])
                # if self.crossover_short>0:
                #     amount_to_invest = 0.25*self.broker.cash
                #     self.size = math.floor(amount_to_invest / self.data.close)
                #     self.sell(size = self.size)
                #     self.countrade +=1
                #     self.log('SHORT SELL created, %.2f' % self.dataclose[0])

            elif self.position.size >0:
                # SAR turn bearish
                if self.SARbull<0:
                    self.order = self.close()
                    self.log('SELL created, %.2f' % self.datas[0].close[0])
                    return
                # strong trend ends, must sell
                if self.onUptrend<1:
                    self.order = self.close()
                    self.log('SELL created, %.2f' % self.datas[0].close[0])
                    return
                # SAR trailing stop
                self.order = self.sell(price = min(self.datas[0].close[-1],self.datas[0].close[-2]) ,exectype= backtrader.Order.Stop , valid=backtrader.Order.DAY )
            #     # amount_to_invest = 0.25*self.broker.cash
            #     # self.size = math.floor(amount_to_invest / self.data.close)
            #     # self.sell(size = self.size)
            #     # self.countrade +=1
            #     # self.log('SHORT SELL created, %.2f' % self.dataclose[0])
            # if self.crossover_short_exit<0 and self.position.size<0:
            #     self.close()
            #     self.log('BUY TO RECOVER created, %.2f' % self.dataclose[0])
                # amount_to_invest = self.params.order_percentage*self.broker.cash
                # self.size = math.floor(amount_to_invest / self.data.close)
                # self.buy(size = self.size)
                # self.countrade +=1
                # self.log('BUY created, %.2f' % self.dataclose[0])
                
                


    def output_value(self):
        return self.countrade

    def get_win_rate(self):
        if not self.trades:
            return 0.0
        winning_trades = sum(1 for trade in self.trades if trade.pnl > 0)
        win_rate = (winning_trades / len(self.trades)) * 100
        return win_rate