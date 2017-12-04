import heapq


class MinHeap(object):
    def __init__(self): self.h = []

    def heappush(self, item): heapq.heappush(self.h, item)

    def heappop(self): return heapq.heappop(self.h)

    def heapreplace(self, item): return heapq.heapreplace(self.h, item)

    def __getitem__(self, i): return self.h[i]

    def __len__(self): return len(self.h)

