import unittest

from model.src.main.book.book import Book
from model.src.main.book.level import Level
from model.src.main.strategy.mbl import MBL
from model.src.main.strategy.mbl_update import MBLUpdate


class TestMBL(unittest.TestCase):

    def test_adds_bid_to_empty_book_when_update_on_bid(self):
        book = Book()
        bid_update = MBLUpdate(13.1, 4, 126)

        mbl = MBL(5)
        updated_book = mbl.update(book, bid_update)

        expected_book = Book()
        expected_book.add_bid(Level(13.1, 4, 126))
        self.assertEqual(expected_book, updated_book)

    def test_updates_existing_bid_level_when_update_on_bid(self):
        book = Book()
        book.add_bid(Level(13.1, 2, 7))
        bid_update = MBLUpdate(13.1, 4, 126)

        mbl = MBL(5)
        updated_book = mbl.update(book, bid_update)

        expected_book = Book()
        expected_book.add_bid(Level(13.1, 4, 126))
        self.assertEqual(expected_book, updated_book)

    def test_cut_extra_levels_when_update_on_full_bid(self):
        book = Book()
        book.add_bid(Level(15.1, 1, 2))
        book.add_bid(Level(13.1, 1, 2))
        bid_update = MBLUpdate(17.1, 1, 2)

        mbl = MBL(length=2)
        updated_book = mbl.update(book, bid_update)

        expected_book = Book([Level(17.1, 1, 2), Level(15.1, 1, 2)], [])
        self.assertEqual(expected_book, updated_book)

    def test_deletes_existing_level_when_update_on_bid(self):
        book = Book()
        book.add_bid(Level(13.1, 1, 2))
        book.add_bid(Level(15.1, 1, 2))
        delete_bid = MBLUpdate.create_delete_bid_level(13.1)

        mbl = MBL(5)
        updated_book = mbl.update(book, delete_bid)

        expected_book = Book([Level(15.1, 1, 2)], [])
        self.assertEqual(expected_book, updated_book)

    def test_keeps_book_intact_when_delete_missing_level(self):
        book = Book()
        book.add_bid(Level(13.1, 1, 2))
        book.add_bid(Level(15.1, 1, 2))
        delete_bid = MBLUpdate.create_delete_bid_level(18.1)

        mbl = MBL(5)
        updated_book = mbl.update(book, delete_bid)

        expected_book = Book([Level(13.1, 1, 2), Level(15.1, 1, 2)], [])
        self.assertEqual(expected_book, updated_book)

    def test_keeps_book_intact_when_delete_on_empty_book(self):
        empty_book = Book()
        delete_bid = MBLUpdate.create_delete_bid_level(18.1)

        mbl = MBL(5)
        updated_book = mbl.update(empty_book, delete_bid)

        expected_book = Book()
        self.assertEqual(expected_book, updated_book)

    def test_updates_existing_bid(self):
        book = Book()
        book.add_bid(Level(11705.0, 1, 0.381988))
        book.add_bid(Level(11704.0, 4, 0.955999))
        book.add_bid(Level(11703.0, 1, 0.165141))

        print(book)

        mbl = MBL(3)
        bid_update = MBLUpdate(11704.0, 3, 0.94745498)
        updated_book = mbl.update(book, bid_update)
        print(updated_book)

        expected_book = Book()
        expected_book.add_bid(Level(11705.0, 1, 0.381988))
        expected_book.add_bid(Level(11704.0, 3, 0.94745498))
        expected_book.add_bid(Level(11703.0, 1, 0.165141))
        self.assertEqual(expected_book, updated_book)

