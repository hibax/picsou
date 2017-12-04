from unittest import TestCase

from model.src.main.book.level import Level
from model.src.main.strategy.mbl_snapshot import MBLSnapshot


class TestMBLSnapshot(TestCase):

    def test_splits_full_snapshot(self):
        snapshot = [[10.0, 1, 2.5], [11.5, 1, 2], [15.0, 1, -2], [18.2, 1, -6.3]]
        mbl_snapshot = MBLSnapshot(snapshot)
        (bid, ask) = mbl_snapshot.split()
        self.assertEqual([Level(10.0, 1, 2.5), Level(11.5, 1, 2)], bid)
        self.assertEqual([Level(15.0, 1, 2), Level(18.2, 1, 6.3)], ask)
