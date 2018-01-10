
def encode_book(book):
    return [[encode_level(level) for level in book.bid], [encode_level(level) for level in book.ask]]


def encode_level(level):
    return [level.price, level.count, level.amount]


def encode_trades(trades):
    return []
