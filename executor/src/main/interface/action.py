from enum import Enum


class Order(Enum):
    BUY = 1
    SELL = 2
    CANCEL = 3


class Action(object):

    def __init__(self, order, product):
        self.order = order
        self.product = product

