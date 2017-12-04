import heapq


class MaxHeap(object):

    def __init__(self): self.h = []

    def __eq__(self, other):
        return self.h == other.h

    def heappush(self, item): heapq.heappush(self.h, MaxHeap.MaxHeapItem(item))

    def heappop(self): return heapq.heappop(self.h).value

    def heapreplace(self, item): return heapq.heapreplace(self.h, MaxHeap.MaxHeapItem(item)).value

    def __getitem__(self, i): return self.h[i].value

    def __len__(self): return len(self.h)

    class MaxHeapItem(object):
        def __init__(self, value): self.value = value

        def __lt__(self, other): return self.value > other.value

        def __eq__(self, other): return self.value == other.value

        def __str__(self): return str(self.value)
