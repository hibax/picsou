import operator

from model.src.main.book.level import Level
from model.src.main.trade.trade import Trade
from model.src.main.trade.trades import Trades


def trade(amount, price, mts=0):
    return [0, mts, amount, price]


def to_trade(t):
    return Trade(t[1], t[2], t[3])


def execute_top_sell(book, buy_order):
    sold_amount = 0
    trades = []

    while sold_amount < buy_order.amount and len(book.ask) != 0:
        top_sell = book.ask[0]
        rest = buy_order.amount - sold_amount

        if rest < top_sell.amount:
            executed_amount = top_sell.amount - rest
            book.ask[0] = Level(top_sell.price, min(top_sell.count - 1, 1), executed_amount)
            trades.append(trade(executed_amount, top_sell.price))
            sold_amount += executed_amount
        else:
            sold_amount += top_sell.amount
            trades.append(trade(top_sell.amount, top_sell.price))
            book.ask = book.ask[1:]

    return trades, book


def apply_matched_asks(book, matched_asks):
    asks = book.ask
    for matched_ask in matched_asks:
        for ask in asks:
            if matched_ask.price == ask.price:
                ask.amount -= matched_ask.amount
                ask.count = min(ask.count - 1, 1)

    book.ask = [ask for ask in asks if ask.amount > 0]
    return book


def build_events(trades, updated_book):
    if len(trades) > 0:
        return [{'event_name': 'on_trade', 'data': Trades(trades)},
                {'event_name': 'on_mbl', 'data': updated_book}]
    else:
        return [{'event_name': 'on_mbl', 'data': updated_book}]


class Simulation(object):

    def __init__(self):
        self.matched_asks = []
        self.matched_bids = []
        self.market_buy_orders = []
        self.market_sell_orders = []
        self.buy_orders = []
        self.sell_orders = []

    def on_event(self, event):
        fct = operator.methodcaller(event['event_name'], event['data'])
        return fct(self)

    def on_mbl(self, book):
        trades = []
        updated_book = book
        
        if len(self.market_buy_orders) > 0:
            trades, updated_book = execute_top_sell(book, self.market_buy_orders.pop(0))
            
        if len(self.matched_asks) > 0:
            updated_book = apply_matched_asks(updated_book, self.matched_asks)

        self.matched_asks.extend([to_trade(t) for t in trades])

        return build_events(trades, updated_book)

    def on_action(self, action):
        fct = operator.methodcaller(action['type'], action)
        fct(self)

    def add_buy_order(self, action):
        if action['order'].price == -1:
            self.market_buy_orders.append(action['order'])
        else:
            self.buy_orders.append(action['order'])
