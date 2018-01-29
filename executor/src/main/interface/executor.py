

class Executor(object):

    def add_buy_order(self, action):
        print("Buying " + action['product'] + " at " + str(action['order'].price) + "USD")

    def add_sell_order(self, action):
        print("Selling " + action['product'] + " at " + str(action['order'].price) + "USD")

    def cancel_order(self, action):
        print("Cancelling " + action['order_id'] + ' on ' + action['product'])
