from scripts.lim import limerickly

def test_api():
    lim = limerickly()
    res = lim.get_rhymes("Cute", 5)
    assert len(res) == 5