from executor.src.main.interface.action import Order


class Executor(object):

    def execute(self, action):

        if action is None:
            return

        bids = action.product.order_book.bid
        asks = action.product.order_book.ask

        if len(bids) < 1 or len(asks) < 1:
            print("???")
            return

        if action.order == Order.BUY:
            price = bids[0].price - 0.01
            print("Buying " + action.product.product_id + " at " + str(price) + "USD")

        elif action.order == Order.SELL:
            price = asks[0].price + 0.01
            print("Selling " + action.product.product_id + " at " + str(price) + "USD")

        elif action.order == Order.CANCEL:
            print("Cancelling orders for " + action.product.product_id)

    def add_order(self, order):
        pass

    def cancel_order(self, cancellation):
        pass
