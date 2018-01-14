import json
from unittest import TestCase

from engine.src.main.recorder.recorder import Recorder
from model.src.main.book.book import Book
from model.src.main.book.level import Level
from model.src.main.trade.trades import Trades


class TestRecorder(TestCase):
    class TestOutputStream(object):
        def __init__(self):
            self.dump = ""

        def write(self, json_dump):
            self.dump += json_dump

    def test_on_mbl(self):
        os = TestRecorder.TestOutputStream()
        book = Book(bids=[Level(10.0, 1, 2.5), Level(11.5, 1, 2)], asks=[Level(15.0, 1, 2), Level(18.2, 1, 6.3)])

        recorder = Recorder(os)
        recorder.on_mbl(book)

        self.assertEqual(json.dumps({'event_name': 'on_mbl', 'data': {'bid': [[10.0, 1, 2.5], [11.5, 1, 2]], 'ask': [[15.0, 1, 2], [18.2, 1, 6.3]]}}) + "\n", os.dump)

    def test_on_trade(self):
        os = TestRecorder.TestOutputStream()
        trades = Trades(trades=[(0, 10.0, 1, 2.5), (0, 11.5, 1, 2)], length=2)

        recorder = Recorder(os)
        recorder.on_trade(trades)

        self.assertEqual(
            json.dumps({'event_name': 'on_trade', 'data': [[10.0, 1, 2.5], [11.5, 1, 2]]}) + "\n",
            os.dump)
