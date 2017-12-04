import json

from websocket import create_connection

from model.src.main.book.book import Book
from model.src.main.strategy.mbl import MBL
from model.src.main.strategy.mbl_snapshot import MBLSnapshot
from model.src.main.strategy.mbl_update import MBLUpdate


def main():
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

    ws.close()


if __name__ == '__main__':
    main()
