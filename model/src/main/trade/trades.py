from bisect import bisect_right
from model.src.main.trade.trade import Trade


class Trades(object):
    def __init__(self, trades=None, length=25):
        self.length = length
        self.trades = [Trade(trade[1], trade[2], trade[3]) for trade in trades[:length]] if trades else []

    def __str__(self):
        r = '\n'.join(str(trade) for trade in self.trades)
        header = "{0:^40}".format('TRADE')
        return header + '\n' + r

    def add_trade(self, trade):
        if trade.mts >= self.trades[0].mts:
            self.trades.insert(0, trade)
        else:
            insert_index = bisect_right(self.trades[::-1], trade)
            self.trades.insert(len(self.trades) - insert_index, trade)
        if len(self.trades) > self.length:
            self.trades.pop()

    def get_last_trade(self):
        return self.trades[0]
