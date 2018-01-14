import unittest

from model.src.main.algo.min_heap import MinHeap
import operator

def extract_content(heap):
    return [heap.heappop() for i in range(len(heap))]

class A(object):
    def mth(self):
        print('A')

class B(A):
    def mth(self):
        print('B')


class TestMinHeap(unittest.TestCase):

    def test_heappush_sorts_a_list(self):
        unsorted_values = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
        min_heap = MinHeap()
        for value in unsorted_values:
            min_heap.heappush(value)

        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], extract_content(min_heap))

    def test_min_heap_returns_first_element(self):
        min_heap = MinHeap()
        min_heap.heappush(9)

        self.assertEqual(9, min_heap[0])

    def test_min_heap_maintains_min(self):
        min_heap = MinHeap()
        min_heap.heappush(9)
        min_heap.heappush(2)

        self.assertEqual(2, min_heap[0])

    def test_min_heap_keep_first_if_smaller(self):
        min_heap = MinHeap()
        min_heap.heappush(2)
        min_heap.heappush(9)

        self.assertEqual(2, min_heap[0])

    def test_min_heap_replace_maintains_heap_prop(self):
        min_heap = MinHeap()
        min_heap.heappush(7)
        min_heap.heappush(3)
        min_heap.heappush(4)
        min_heap.heappush(8)
        min_heap.heappush(6)
        self.assertEqual(3, min_heap.heapreplace(5))

        self.assertEqual([4, 5, 6, 7, 8], extract_content(min_heap))

    def test_call_child_method(self):
        b = B()

        m = operator.methodcaller('mth')

        m(b)

        ls = (l for l in open('max_heap_test.py', 'r'))
        for l in ls:
            print(l)

