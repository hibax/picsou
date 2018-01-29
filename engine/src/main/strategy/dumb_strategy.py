from engine.src.main.strategy.strategy import Strategy
from executor.src.main.interface import actions


class DumbStrategy(Strategy):

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

        action = None

        if len(book.ask) > 0 and len(book.bid) > 0:
            if asks_amount < bids_amount:
                action = actions.buy("BTC-USD", 1, book.bid[0].price - 0.01)
            else:
                action = actions.sell("BTC-USD", 1, book.ask[0].price + 0.01)

        return action
