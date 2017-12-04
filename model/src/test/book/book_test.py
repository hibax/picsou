import unittest

from model.src.main.book.book import Book
from model.src.main.book.level import Level
from model.src.main.book.order import Order


class TestBook(unittest.TestCase):

    def test_default_book_is_empty(self):
        book = Book()
        self.assertTrue(book.is_empty())

    def test_len_is_zero_for_default_book(self):
        book = Book()
        self.assertEqual(0, len(book))

    def test_best_bid_is_the_greatest_price(self):
        book = Book()
        book.add_bid(Order(7, 10))
        book.add_bid(Order(5, 10))
        self.assertEqual(Order(7, 10), book.best_bid())

    def test_best_ask_is_the_smallest_price(self):
        book = Book()
        book.add_ask(Order(5, 10))
        book.add_ask(Order(7, 10))
        self.assertEqual(Order(5, 10), book.best_ask())

    def test_a_book_with_three_bid_lines_has_a_bid_depth_of_three(self):
        book = Book()
        book.add_bid(Level(7, 10, 2))
        book.add_bid(Level(5, 10, 2))
        book.add_bid(Level(4, 10, 2))
        self.assertEqual(3, book.bid_depth())

    def test_a_book_with_three_ask_lines_has_a_ask_depth_of_three(self):
        book = Book()
        book.add_ask(Level(4, 10, 2))
        book.add_ask(Level(5, 10, 2))
        book.add_ask(Level(7, 10, 2))
        self.assertEqual(3, book.ask_depth())

    @unittest.skip
    def test_displays_nicely_an_unaligned_book(self):
        book = Book()
        book.add_bid(Order(6.3, 80))
        book.add_bid(Order(4, 5))
        book.add_ask(Order(7, 1))
        book.add_ask(Order(10, 150))
        book.add_ask(Order(16, 42))

        expected_str = "              BID              |              ASK              \n" \
                       "     +6.300000 x     80.000000 |     +7.000000 x      1.000000\n" \
                       "     +4.000000 x      5.000000 |    +10.000000 x    150.000000\n" \
                       "                               |    +16.000000 x     42.000000"

        self.assertEqual(expected_str, str(book))

    def test_displays_nicely_a_MBL(self):
        book = Book()
        book.add_bid(Level(6.3, 4, 80))
        book.add_bid(Level(4, 1, 5))
        book.add_ask(Level(7, 1, 1))
        book.add_ask(Level(10, 26, 150))
        book.add_ask(Level(16, 17, 42))

        expected_str = "                  BID                   |                  ASK                  \n" \
                       "     +6.300000 x     80.000000 @      4 |     +7.000000 x      1.000000 @      1\n" \
                       "     +4.000000 x      5.000000 @      1 |    +10.000000 x    150.000000 @     26\n" \
                       "                                        |    +16.000000 x     42.000000 @     17"

        self.assertEqual(expected_str, str(book))


if __name__ == '__main__':
    unittest.main()
