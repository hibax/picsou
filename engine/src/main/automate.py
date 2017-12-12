from engine.src.main.strategy.strategy import Strategy
from engine.src.main.trading.trading_engine import TradingEngine


def start_engine(in_queue, out_queue):
    strategy = Strategy()  # we should instantiate the desired strategy instead of the interface
    engine = TradingEngine(strategy)

    while True:
        fct, msg = in_queue.get()

        action = fct(engine, msg)

        out_queue.put((msg, action))

