import operator

from engine.src.main.strategy.strategy import Strategy
from engine.src.main.trading.trading_engine import TradingEngine


def start_engine(in_queue, out_queue):
    strategy = Strategy()  # we should instantiate the desired strategy instead of the interface
    engine = TradingEngine(strategy)

    try:
        while True:
            fct_name, msg = in_queue.get()
            fct = operator.methodcaller(fct_name, msg)
            action = fct(engine)
            out_queue.put((msg, action))

    except KeyboardInterrupt:
        print("Keyboard interruption in trading engine")

    finally:
        print("Cleaning trade engine")

