import unittest
from unittest.mock import patch, mock_open
from main import get_joke

class JokeTesting(unittest.TestCase):
    def test_joke_length(self):
        joke = get_joke()
        self.assertGreater(len(joke), 80)
    
    @patch('builtins.open', new_callable=mock_open, read_data='[{"joke": "Joke 1"}, {"joke": "Joke 2"}, {"joke": "Joke 3"}]')
    def test_joke_random_choosing(self, mock_file):
        joke = get_joke()
        mock_file.assert_called_once_with("jokes.json", 'r')
        self.assertIn(joke, ["Joke 1", "Joke 2", "Joke 3"])
        

if __name__ == 'main':
    unittest.main()
