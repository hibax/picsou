import unittest

from model.src.main.algo.max_heap import MaxHeap


def extract_content(heap):
    return [heap.heappop() for _ in range(len(heap))]


class TestMaxHeap(unittest.TestCase):

    def test_heappush_sorts_a_list(self):
        unsorted_values = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
        max_heap = MaxHeap()
        for value in unsorted_values:
            max_heap.heappush(value)

        self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], extract_content(max_heap))

    def test_max_heap_returns_first_element(self):
        max_heap = MaxHeap()
        max_heap.heappush(9)

        self.assertEqual(9, max_heap[0])

    def test_max_heap_maintains_max(self):
        max_heap = MaxHeap()
        max_heap.heappush(9)
        max_heap.heappush(2)

        self.assertEqual(9, max_heap[0])

    def test_max_heap_keeps_first_if_greater(self):
        max_heap = MaxHeap()
        max_heap.heappush(2)
        max_heap.heappush(9)

        self.assertEqual(9, max_heap[0])

    def test_max_heap_replace_maintains_heap_prop(self):
        max_heap = MaxHeap()
        max_heap.heappush(7)
        max_heap.heappush(3)
        max_heap.heappush(4)
        max_heap.heappush(8)
        max_heap.heappush(6)
        self.assertEqual(8, max_heap.heapreplace(5))

        self.assertEqual([7, 6, 5, 4, 3], extract_content(max_heap))
