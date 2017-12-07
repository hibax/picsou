import json

import logging
import time
import sys

from websocket import create_connection

from engine.src.main.recorder.recorder import Recorder
from model.src.main.book.book import Book
from model.src.main.strategy.mbl import MBL
from model.src.main.strategy.mbl_snapshot import MBLSnapshot
from model.src.main.strategy.mbl_update import MBLUpdate

from btfxwss import BtfxWss


def main():
    btfxwss()


def home_made_websocket():
    ws = create_connection("wss://api.bitfinex.com/ws/2")

    # Waiting connection
    connected = False
    while not connected:
        result = ws.recv()
        if result:
            connected = True
            result = json.loads(result)
            print("Connection established to Bitfinex api version %s " % result['version'])
        else:
            print("Waiting connection...")

    # Subscribe
    ws.send(json.dumps({
        "event": "subscribe",
        "channel": "book",
        "symbol": "tBTCUSD",
        "prec": "P0",
        "freq": "F0",
        "len": "25"
    }))
    subscribed = False
    while not subscribed:
        result = ws.recv()
        if result:
            subscribed = True
            result = json.loads(result)
            print("Subscribed to %s channel for %s" % (result['channel'], result['pair']))
        else:
            print("Waiting response...")

    mbl = MBL()
    book = Book()


    while True:
        result = ws.recv()
        result = json.loads(result)

        if len(result[1]) > 3:
            print("snapshot")
            mbl_snapshot = MBLSnapshot(result[1])
            book = mbl.from_snapshot(mbl_snapshot)
            print(book)
        elif result[1] == 'hb':
            pass
        elif len(result[1]) == 3:
            print("update: " + str(result[1]))
            update = MBLUpdate(result[1][0], result[1][1], result[1][2])
            book = mbl.update(book, update)
            print(book)


def btfxwss():

    log = logging.getLogger(__name__)

    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)

    log.addHandler(sh)
    log.addHandler(fh)
    logging.basicConfig(level=logging.DEBUG, handlers=[fh, sh])

    wss = BtfxWss()
    wss.start()

    while not wss.conn.connected.is_set():
        time.sleep(1)

    # Subscribe to some channels
    wss.subscribe_to_ticker('BTCUSD')
    wss.subscribe_to_order_book('BTCUSD')
    wss.subscribe_to_order_book('ETHUSD')

    # Wait for subscription...
    time.sleep(2)

    mbl = MBL()
    book = Book()
    recorder = Recorder(open("output.txt", mode='w'))

    # Accessing data stored in BtfxWss:
    books_queue = wss.books('ETHUSD')  # returns a Queue object for the pair.

    while True:

        book_update = books_queue.get()[0][0]

        if len(book_update) > 3:
            print("snapshot")
            mbl_snapshot = MBLSnapshot(book_update)
            book = mbl.from_snapshot(mbl_snapshot)
            recorder.on_mbl(book)

        elif len(book_update) == 3:
            print("update: " + str(book_update))
            update = MBLUpdate(book_update[0], book_update[1], book_update[2])
            book = mbl.update(book, update)
            recorder.on_mbl(book)

    # Unsubscribing from channels:
    wss.unsubscribe_from_ticker('BTCUSD')
    wss.unsubscribe_from_order_book('BTCUSD')

    # Shutting down the client:
    wss.stop()


if __name__ == '__main__':
    main()
