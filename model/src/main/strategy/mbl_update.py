class MBLUpdate(object):
    def __init__(self, price, count, amount):
        self.price = price
        self.count = count
        self.amount = amount

    def is_add_or_update_level(self):
        return self.count > 0

    def is_add_or_update_bid(self):
        return self.amount > 0

    def is_delete_level(self):
        return self.count == 0

    def is_delete_bid(self):
        return self.amount == 1

    def is_delete_ask(self):
        return self.amount == -1

    @staticmethod
    def create_delete_bid_level(price):
        return MBLUpdate(price, 0, 1)

    @staticmethod
    def create_delete_ask_level(price):
        return MBLUpdate(price, 0, -1)
