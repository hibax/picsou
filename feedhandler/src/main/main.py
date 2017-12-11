
import logging
import time
import sys

import asyncio

from engine.src.main.recorder.recorder import Recorder
from feedhandler import start_feed
from model.src.main.book.book import Book
from model.src.main.strategy.mbl import MBL
from model.src.main.strategy.mbl_snapshot import MBLSnapshot
from model.src.main.strategy.mbl_update import MBLUpdate

from btfxwss import BtfxWss

import gdax


def main():
    queue = asyncio.Queue()
    start_feed(queue)


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



def gdax_sandbox():


    auth_client = gdax.AuthenticatedClient("5c8da7518000779d0f02161e447a54f5", "QQdn5e4Ch/BKJXwIl1EcKGSh2uOFYrg5HMy5RJV2cTbjd6XctxDc0PiJa3M+M7pTrMXS2045G9nwfL0NPtL1Vw==", "rravnxe2gea", api_url="https://api-public.sandbox.gdax.com")

    print(auth_client.buy(price='0.10', size='0.01', product_id='BTC-USD'))
    print(auth_client.sell(price='100000.00', size='0.01', product_id='BTC-USD'))

    order_book = auth_client.get_product_order_book('BTC-USD', level=2)
    print("asks: ", order_book["asks"])
    print("bids: ", order_book["bids"])


    my_orders = auth_client.get_orders()

    for order in my_orders[0]:
        if order['side'] == 'sell':
            print("I'm trying to sell " + str(order['size']) + "BTC" + " at " + order['price'] + "$")
        else:
            print("I'm trying to buy " + str(order['size']) + "BTC" + " at " + order['price'] + "$")




if __name__ == '__main__':
    main()
