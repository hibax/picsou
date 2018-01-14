
def encode_book(book):
    return {'bid': [encode_level(level) for level in book.bid], 'ask': [encode_level(level) for level in book.ask]}


def encode_level(level):
    return [level.price, level.count, level.amount]


def encode_trades(trades):
    return [encode_trade(t) for t in trades.trades]


def encode_trade(trade):
    return [trade.mts, trade.amount, trade.price]
