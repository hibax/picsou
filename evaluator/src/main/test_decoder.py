import json
from unittest import TestCase

from evaluator.src.main.decoder import decode
from model.src.main.book.book import Book
from model.src.main.book.level import Level
from model.src.main.trade.trades import Trades


class TestDecode(TestCase):
    def test_decode_book(self):
        record_entry = json.dumps({'event_name': 'on_mbl', 'data': {'bid': [[10.0, 1, 2.5], [11.5, 1, 2]], 'ask': [[15.0, 1, 2], [18.2, 1, 6.3]]}})
        entry = decode(record_entry)
        self.assertEqual({'event_name': 'on_mbl', 'data': Book([Level(10.0, 1, 2.5), Level(11.5, 1, 2)], [Level(15.0, 1, 2), Level(18.2, 1, 6.3)])}, entry)

    def test_decode_trades(self):
        record_entry = json.dumps({'event_name': 'on_trade', 'data': [[10.0, 1, 2.5], [11.5, 1, 2]]})
        entry = decode(record_entry)
        self.assertEqual({'event_name': 'on_trade', 'data': Trades(trades=[(0, 10.0, 1, 2.5), (0, 11.5, 1, 2)])}, entry)
