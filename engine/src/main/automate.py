from engine.src.main.trading.trading_engine import TradingEngine


def start_engine(in_queue, out_queue):
    engine = TradingEngine(None)

    while True:
        fct, msg = in_queue.get()

        fct(engine, msg)

        out_queue.put(msg)

