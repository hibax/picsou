import json

from engine.src.main.interface.engine import Engine
from engine.src.main.recorder.encoder import encode_book
from engine.src.main.recorder.encoder import encode_trades


class Recorder(Engine):

    def __init__(self, output_stream):
        self.output_stream = output_stream

    def on_mbl(self, book):
        self.output_stream.write(json.dumps(encode_book(book)))

    def on_trade(self, trades):
        self.output_stream.write(json.dumps(encode_trades(trades)))

    def on_daily_info(self, info):
        pass
