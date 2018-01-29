from model.src.main.book.order import Order


MARKET_PRICE = -1


def buy(product, amount, price=MARKET_PRICE):
    return {'type': 'add_buy_order', 'order': Order(price, amount), 'product': product}


def sell(product, amount, price=MARKET_PRICE):
    return {'type': 'add_sell_order', 'order': Order(price, amount), 'product': product}


def cancel(product, order_id):
    return {'type': 'cancel_order', 'order': order_id, 'product': product}

