import unittest
from main import get_joke

class TestJoke(unittest.TestCase):
    def test_joke_length(self):
        joke = get_joke()
        self.assertGreater(len(joke), 3)

if __name__ == 'main':
    unittest.main()
