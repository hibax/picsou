class Order(object):
    VOLUME_PRECISION = 6

    def __init__(self, price, amount):
        self.price = price
        self.amount = amount

    def __eq__(self, other):
        return self.price == other.price and self.amount == other.amount

    def __str__(self):
        return "{0:>+14.{precision}f} x {1:>13.{precision}f}" \
            .format(self.price, self.amount, precision=self.VOLUME_PRECISION)
