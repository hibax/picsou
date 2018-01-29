import operator

from engine.src.main.recorder.recorder import Recorder
from engine.src.main.strategy.dumb_strategy import DumbStrategy
from engine.src.main.strategy.strategy import Strategy
from engine.src.main.trading.trading_engine import TradingEngine


def start_engine(in_queue, out_queue, strategy_name):
    strats = {'dumb': DumbStrategy(), 'default': Strategy()}

    if strategy_name not in strats:
        raise KeyError('Cannot find a strategy called ' + strategy_name)

    strategy = strats[strategy_name]
    engine = TradingEngine(strategy)

    try:
        while True:
            event = in_queue.get()
            fct = operator.methodcaller(event['event_name'], event['data'])
            action = fct(engine)
            if action is not None:
                out_queue.put(action)

    except KeyboardInterrupt:
        print("Keyboard interruption in trading engine")

    finally:
        print("Cleaning trade engine")


def start_recorder(in_queue):
    engine = Recorder(open("output.txt", 'w'))

    try:
        while True:
            event = in_queue.get()
            fct = operator.methodcaller(event['event_name'], event['data'])
            fct(engine)

    except KeyboardInterrupt:
        print("Keyboard interruption in trading engine")

    finally:
        print("Cleaning trade engine")

