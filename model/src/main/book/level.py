
class Level(object):
    VOLUME_PRECISION = 6

    def __init__(self, price, count, amount):
        self.price = price
        self.count = count
        self.amount = amount

    def __eq__(self, other):
        return self.price == other.price and self.count == other.count and self.amount == other.amount

    def __gt__(self, other):
        return self.price > other.price

    def __lt__(self, other):
        return self.price < other.price

    def __str__(self):
        return "{0:>+14.{precision}f} x {1:>13.{precision}f} @ {2:>6}"\
            .format(self.price, self.amount, self.count, precision=self.VOLUME_PRECISION)

    @staticmethod
    def bid_header():
        return "{0:^40}".format('BID')

    @staticmethod
    def ask_header():
        return "{0:^39}".format('ASK')
