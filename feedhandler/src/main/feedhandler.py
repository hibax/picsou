import websockets
import asyncio
import json

from model.src.main.book.book import Book
from model.src.main.strategy.mbl import MBL
from model.src.main.strategy.mbl_snapshot import MBLSnapshot
from model.src.main.strategy.mbl_update import MBLUpdate
from model.src.main.trade.trade import Trade
from model.src.main.trade.trades import Trades


def start_feed(in_queue):
    loop = asyncio.new_event_loop()

    try:
        loop.run_until_complete(home_made_websocket(in_queue))

    except KeyboardInterrupt:
        print("Keyboard interruption in feed handler")

    finally:
        print("Cleaning feed handler")


async def home_made_websocket(in_queue):
    async with websockets.connect("wss://api.bitfinex.com/ws/2") as ws:
        result = await ws.recv()
        result = json.loads(result)
        print("Connection established to Bitfinex api version %s " % result['version'])

        # Subscribe
        await ws.send(json.dumps({
            "event": "subscribe",
            "channel": "book",
            "symbol": "tBTCUSD",
            "prec": "P0",
            "freq": "F0",
            "len": "25"
        }))

        # Subscribe
        await ws.send(json.dumps({
            "event": "subscribe",
            "channel": "trades",
            "symbol": "tBTCUSD"
        }))

        mbl = MBL()
        book = Book()
        trades = Trades()
        channel_ids = {}

        try:

            while True:
                result = await ws.recv()
                result = json.loads(result)
                fct_to_call = None
                decoded_msg = Book()
                if 'event' in result and result['event'] == 'subscribed':
                    print("Subscribed to %s channel for %s" % (result['channel'], result['pair']))
                    if result['channel'] == 'book':
                        channel_ids[result['chanId']] = 'b'
                    elif result['channel'] == 'trades':
                        channel_ids[result['chanId']] = 't'
                elif result[0] in channel_ids and channel_ids[result[0]] == 't':
                    if result[1] == 'tu':
                        pass
                    elif result[1] == 'hb':
                        pass
                    elif len(result[1]) > 3:
                        trades = Trades(result[1], length=3)
                        decoded_msg = trades
                        fct_to_call = 'on_trade'
                    elif result[1] == 'te':
                        trades.add_trade(Trade(result[2][1], result[2][2], result[2][3]))
                        decoded_msg = trades
                        fct_to_call = 'on_trade'
                elif result[0] in channel_ids and channel_ids[result[0]] == 'b':
                    if len(result[1]) > 3:
                        mbl_snapshot = MBLSnapshot(result[1])
                        book = mbl.from_snapshot(mbl_snapshot)
                        decoded_msg = book
                        fct_to_call = 'on_mbl'
                    elif result[1] == 'hb':
                        pass
                    elif len(result[1]) == 3:
                        # print("update: " + str(result[1]))
                        update = MBLUpdate(result[1][0], result[1][1], result[1][2])
                        book = mbl.update(book, update)
                        decoded_msg = book
                        fct_to_call = 'on_mbl'

                if fct_to_call is not None:
                    in_queue.put({'event_name': fct_to_call, 'data': decoded_msg})

        except KeyboardInterrupt:
            print("Keyboard interruption in websocket")

        finally:
            print("Cleaning websocket")


