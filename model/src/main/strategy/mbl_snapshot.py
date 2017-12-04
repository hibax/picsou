from itertools import takewhile, islice

from model.src.main.book.level import Level


class MBLSnapshot(object):
    def __init__(self, levels=None):
        self.levels = levels if levels is not None else []

    def split(self):
        bid = [self.to_bid(level) for level in takewhile(lambda level: level[2] > 0, self.levels)]
        ask = [self.to_ask(level) for level in islice(self.levels, len(bid), None)]
        return bid, ask

    def to_bid(self, level):
        return Level(level[0], level[1], level[2])

    def to_ask(self, level):
        return Level(level[0], level[1], -level[2])
