import json

from model.src.main.book.book import Book
from model.src.main.book.level import Level
from model.src.main.trade.trades import Trades


def encode_book(book):
    return {'bid': [encode_level(level) for level in book.bid], 'ask': [encode_level(level) for level in book.ask]}


def encode_level(level):
    return [level.price, level.count, level.amount]


def decode_trades(trades):
    return Trades([[0, t[0], t[1], t[2]] for t in trades])


def decode_levels(levels_str):
    return [Level(l[0], l[1], l[2]) for l in levels_str]


def decode_mbl(book_str):
    return Book(decode_levels(book_str['bid']), decode_levels(book_str['ask']))


def decode(record_entry):
    entry = json.loads(record_entry)
    if entry['event_name'] == 'on_mbl':
        entry['data'] = decode_mbl(entry['data'])
    elif entry['event_name'] == 'on_trade':
        entry['data'] = decode_trades(entry['data'])
    return entry
