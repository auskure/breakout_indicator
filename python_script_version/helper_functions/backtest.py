import pandas as pd
import numpy as np
from backtesting import Strategy
from backtesting import Backtest

class MyStrat_1(Strategy):
    #the first strategy is a naive one. 
    # We simply buy with all our cash when there is a bullish breakout pattern, 
    # and sell with all our cash when there is a bearish breakout pattern.
    # there is only one trade happening at a time
    lot_size = 10000 

    def init(self):
        super().init()

    def next(self):
        super().next()
        TPSLRatio = 2
        perc_for_sl = 0.03
        
        #Close trades if RSI is above 80 for long positions or below 20 for short positions
        for trade in self.trades:
            if trade.is_long and self.data.RSI[-1] > 80:
                trade.close()
            elif trade.is_short and self.data.RSI[-1] < 20:
                trade.close()

        #if no trades currently and there is a bullish breakout pattern
        if len(self.trades)==0 and self.data.pattern_detected==2:
            sl = self.data.Close[-1]-self.data.Close[-1]*perc_for_sl
            sldiff = abs(sl-self.data.Close[-1])
            tp = self.data.Close[-1]+sldiff*TPSLRatio
            self.buy(sl=sl, tp=tp, size=self.lot_size)

        #if no trades currently and there is a bearish breakout pattern
        elif len(self.trades)==0 and self.data.pattern_detected==1:         
            sl = self.data.Close[-1]+self.data.Close[-1]*perc_for_sl
            sldiff = abs(sl-self.data.Close[-1])
            tp = self.data.Close[-1]-sldiff*TPSLRatio
            self.sell(sl=sl, tp=tp, size=self.lot_size)



class MyStrat_2(Strategy):
    #the second strategy more complex.
    # Like the first strategy, we buy with all our cash when there is a bullish breakout pattern, 
    # and sell when there is a bearish breakout pattern.
    # 2 trades will be executed, with different take profit levels.
    # When the lower take profit level has been reached, the trade with the higher take profit level
    # will be updated to have a higher stop loss.  This is to allow for profits to roll more.
    # there is only one trade happening at a time
    lot_size = 0.99
    def init(self):
        super().init()

    def next(self):
        super().next()
        TPSLRatio = 3
        perc_for_sl = 0.03

        #if there is only one trade left, a take profit has been activated and a bigger risk can be taken.
        if len(self.trades)==1:
            for trade in self.trades:
                trade.sl = trade.entry_price
                
        if len(self.trades)==0 and self.data.pattern_detected==2:
            sl1 = self.data.Close[-1]-self.data.Close[-1]*perc_for_sl
            sldiff = abs(sl1-self.data.Close[-1])
            tp1 = self.data.Close[-1]+sldiff*TPSLRatio
            tp2 = self.data.Close[-1]+sldiff
            self.buy(sl=sl1, tp=tp1, size=self.lot_size)
            self.buy(sl=sl1, tp=tp2, size=self.lot_size)
        
        elif len(self.trades)==0 and self.data.pattern_detected==1:         
            sl1 = self.data.Close[-1]+self.data.Close[-1]*perc_for_sl
            sldiff = abs(sl1-self.data.Close[-1])
            tp1 = self.data.Close[-1]-sldiff*TPSLRatio
            tp2 = self.data.Close[-1]-sldiff
            self.sell(sl=sl1, tp=tp1, size=self.lot_size)
            self.sell(sl=sl1, tp=tp1, size=self.lot_size)