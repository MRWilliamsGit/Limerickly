from helpers import get_rhyme

def test_api():
    res = get_rhyme("Cute", 5)
    assert len(res) == 5