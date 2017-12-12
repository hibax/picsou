from engine.src.main.interface.engine import Engine
from model.src.main.book.book import Book
from model.src.main.daily.daily_info import DailyInfo
from model.src.main.trade.trades import Trades


class TradingEngine(Engine):

    def __init__(self, strategy):
        self.book = Book()
        self.trades = Trades()
        self.daily_info = DailyInfo()
        self.living_orders = []
        self.strategy = strategy

    def get_env(self):
        return {"book": self.book, "trades": self.trades, "daily_info": self.daily_info, "living_orders": self.living_orders}

    def on_mbl(self, book):
        self.book = book
        action = self.strategy.produce_action(env=self.get_env())
        self.update_orders(action)
        return action

    def on_trade(self, trades):
        self.trades = trades
        action = self.strategy.produce_action(env=self.get_env())
        self.update_orders(action)
        return action

    def on_daily_info(self, info):
        self.daily_info = info
        action = self.strategy.produce_action(env=self.get_env())
        self.update_orders(action)
        return action

    def update_orders(self, action):
        pass
