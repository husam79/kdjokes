import pytest
from main import get_joke

def test_joke_length():
    joke = get_joke()
    assert len(joke) > 1

    
