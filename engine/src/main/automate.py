import operator

from engine.src.main.recorder.recorder import Recorder
from engine.src.main.strategy.strategy import Strategy
from engine.src.main.trading.trading_engine import TradingEngine


def start_engine(in_queue, out_queue):
    strategy = Strategy()  # we should instantiate the desired strategy instead of the interface
    engine = TradingEngine(strategy)

    try:
        while True:
            event = in_queue.get()
            fct = operator.methodcaller(event['event_name'], event['data'])
            action = fct(engine)
            out_queue.put((event['data'], action))

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

