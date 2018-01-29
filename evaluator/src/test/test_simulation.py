from unittest import TestCase

from evaluator.src.main.Simulation import Simulation
from executor.src.main.interface import actions
from model.src.main.book.book import Book
from model.src.main.book.level import Level
from model.src.main.trade.trades import Trades


class TestSimulation(TestCase):
    def test_buy_market_decreases_top_ask(self):
        simulation = Simulation()
        buy_at_market_price = actions.buy('BTC-USD', 2)
        simulation.on_action(buy_at_market_price)

        mbl = Book(bids=[Level(90, 1, 1)], asks=[Level(100, 2, 5)])

        events = simulation.on_event({'event_name': 'on_mbl', 'data': mbl})

        trade_event = events[0]
        mbl_event = events[1]

        self.assertEqual({'event_name': 'on_trade', 'data': Trades([(0, 0, 2, 100)])}, trade_event)
        self.assertEqual({'event_name': 'on_mbl', 'data': Book(bids=[Level(90, 1, 1)], asks=[Level(100, 1, 3)])}, mbl_event)

    def test_buy_market_removes_top_ask(self):
        simulation = Simulation()
        buy_at_market_price = actions.buy('BTC-USD', 2)
        simulation.on_action(buy_at_market_price)

        mbl = Book(bids=[Level(90, 1, 1)], asks=[Level(100, 1, 1), Level(105, 2, 2)])

        events = simulation.on_event({'event_name': 'on_mbl', 'data': mbl})

        trade_event = events[0]
        mbl_event = events[1]

        self.assertEqual({'event_name': 'on_trade', 'data': Trades([(0, 0, 1, 100), (0, 0, 1, 105)])}, trade_event)
        self.assertEqual({'event_name': 'on_mbl', 'data': Book(bids=[Level(90, 1, 1)], asks=[Level(105, 1, 1)])}, mbl_event)

    def test_new_top_ask_after_buy_market_keeps_it(self):
        simulation = Simulation()
        buy_at_market_price = actions.buy('BTC-USD', 1)
        simulation.on_action(buy_at_market_price)

        mbl = Book(bids=[Level(90, 1, 1)], asks=[Level(105, 2, 2)])
        simulation.on_event({'event_name': 'on_mbl', 'data': mbl})

        mbl_new_top = Book(bids=[Level(90, 1, 1)], asks=[Level(100, 1, 1), Level(105, 2, 2)])
        events = simulation.on_event({'event_name': 'on_mbl', 'data': mbl_new_top})

        mbl_event = events[0]

        self.assertEqual(1, len(events))
        self.assertEqual({'event_name': 'on_mbl', 'data': Book(bids=[Level(90, 1, 1)], asks=[Level(100, 1, 1), Level(105, 1, 1)])}, mbl_event)
