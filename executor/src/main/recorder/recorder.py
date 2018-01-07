from executor.src.main.interface.executor import Executor


class Recorder(Executor):
    def __init__(self, output_stream):
        self.output_stream = output_stream

    def add_order(self, order):
        pass

    def cancel_order(self, cancellation):
        pass
