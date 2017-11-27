import json
import datetime

from websocket import create_connection
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
    "channel": "trades",
    "symbol": "tBTCUSD",
    "pair": "BTCUSD"
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


# Trades
while True:
    result = ws.recv()
    result = json.loads(result)

    if len(result) > 2:
        trade = result[2]
        if trade[2] > 0:
            print("%s - BUY %s BTC (%s$)" % (datetime.datetime.fromtimestamp(trade[1]/1000.0), trade[2], trade[3]))
        else:
            print("%s - SELL %s BTC (%s$)" % (datetime.datetime.fromtimestamp(trade[1]/1000.0), -trade[2], trade[3]))





ws.close()
