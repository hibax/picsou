
class Trade(object):
    VOLUME_PRECISION = 6

    def __init__(self, mts, amount, price):
        self.mts = mts
        self.amount = amount
        self.price = price

    def __eq__(self, other):
        return self.mts == other.mts

    def __gt__(self, other):
        return self.mts > other.mts

    def __lt__(self, other):
        return self.mts < other.mts

    def __str__(self):
        return "{0:>+14.{precision}f} x {1:>13.{precision}f} @ {2:>6}"\
            .format(self.price, self.amount, self.mts, precision=self.VOLUME_PRECISION)
