from executor.src.main.interface.executor import Executor


class Recorder(Executor):
    def __init__(self, output_stream):
        self.output_stream = output_stream

    def add_buy_order(self, action):
        pass

    def add_sell_order(self, action):
        pass

    def cancel_order(self, cancellation):
        pass
