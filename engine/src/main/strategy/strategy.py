
from executor.src.main.interface.action import Action, Order
from model.src.main.product.product import Product


class Strategy(object):

    def produce_action(self, env):

        book = env['book']

        asks_amount = 0
        bids_amount = 0

        for ask in book.ask:
            asks_amount += ask.amount

        for bid in book.bid:
            bids_amount += bid.amount

        print("total bids : " + str(bids_amount))
        print("total asks : " + str(asks_amount))

        if asks_amount < bids_amount:
            order = Order.BUY
        else:
            order = Order.SELL

        product = Product("BTC-USD", book)

        return Action(order, product)
