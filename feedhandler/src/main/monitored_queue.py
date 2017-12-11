

class MonitoredQueue(object):

    def __init__(self, queue):
        self.queue = queue
        self.nb_in = 0
        self.nb_out = 0

    def put(self, item):
        self.nb_in += 1
        self.queue.put(item)

    def get(self):
        self.nb_out += 1
        return self.queue.get()

    def qsize(self):
        return self.queue.qsize()
