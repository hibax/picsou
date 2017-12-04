from bisect import bisect_left

from copy import deepcopy

from model.src.main.book.book import Book
from model.src.main.book.level import Level


class MBL(object):

    def __init__(self, length=25):
        self.length = length

    def from_snapshot(self, snapshot):
        (bid, ask) = snapshot.split()
        return Book(bid[:self.length], ask[:self.length])

    def update(self, book, update_mbl):

        updated_book = Book()

        if update_mbl.is_add_or_update_level():
            if update_mbl.is_add_or_update_bid():
                updated_book = self.add_or_update_bid(book, update_mbl)
            else:
                updated_book = self.add_or_update_ask(book, update_mbl)
        else:
            if update_mbl.is_delete_bid():
                updated_book = self.delete_bid(book, update_mbl.price)
            elif update_mbl.is_delete_ask():
                updated_book = self.delete_ask(book, update_mbl.price)

        return updated_book

    def add_or_update_bid(self, book, update_mbl):
        bid = self.add_or_update(book.bid, update_mbl, lambda l, level: max(len(l) - 1 - bisect_left(l[::-1], level), 0))
        return Book(bid, book.ask)

    def add_or_update_ask(self, book, update_mbl):
        ask = self.add_or_update(book.ask, update_mbl, bisect_left)
        return Book(book.bid, ask)

    def add_or_update(self, levels, update_mbl, find_position):
        new_levels = deepcopy(levels)

        target_level = Level(update_mbl.price, update_mbl.count, abs(update_mbl.amount))
        price_level = find_position(new_levels, target_level)

        is_update = price_level != len(levels) and new_levels[price_level].price == target_level.price

        if is_update:
            new_levels[price_level] = target_level
        else:
            new_levels.insert(price_level, target_level)

        if len(new_levels) > self.length:
            new_levels.pop(len(levels))

        return new_levels

    def delete_bid(self, book, up_price):
        bid = self.delete(book.bid, up_price)
        return Book(bid, book.ask)

    def delete_ask(self, book, up_price):
        ask = self.delete(book.ask, up_price)
        return Book(book.bid, ask)

    def delete(self, levels, price_level):
        new_levels = deepcopy(levels)

        target_level = Level(price_level, 0, 0)
        level_index = bisect_left(new_levels, target_level)

        is_found = level_index != len(levels) and new_levels[level_index].price == target_level.price

        if is_found:
            new_levels.pop(level_index)

        return new_levels
