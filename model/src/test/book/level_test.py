import copy
import unittest

from model.src.main.book.level import Level


class TestLevel(unittest.TestCase):

    def test_two_copies(self):
        original = [Level(1, 2, 3), Level(4, 5, 6)]
        copied_and_changed = copy.deepcopy(original)
        copied_and_changed[0].price = 0
        self.assertNotEqual(original, copied_and_changed)
