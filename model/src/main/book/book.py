from itertools import zip_longest

from model.src.main.book.level import Level


class Book(object):
    PRICE_PRECISION = 6
    VOLUME_PRECISION = 6
    VOLUME_NB_FIGURES = 7
    PRICE_NB_FIGURES = 6
    MULTIPLIER_SIGN_SIZE = 1

    def __init__(self, bids=None, asks=None):
        self.bid = bids if bids is not None else []
        self.ask = asks if asks is not None else []

    def __len__(self):
        return max(len(self.bid), len(self.ask))

    def __eq__(self, other):
        return self.bid == other.bid and self.ask == other.ask

    def is_empty(self):
        return len(self) == 0

    def add_bid(self, line):
        self.bid.append(line)

    def best_bid(self):
        return self.bid[0]

    def add_ask(self, line):
        self.ask.append(line)

    def best_ask(self):
        return self.ask[0]

    def bid_depth(self):
        return len(self.bid)

    def ask_depth(self):
        return len(self.ask)

    def __str__(self):
        r = '\n'.join(str(left) + ' |' + str(right) for left, right in zip_longest(self.bid, self.ask, fillvalue=' ' * 39))

        header = Level.bid_header() + "|" + Level.ask_header()

        return header + '\n' + r
