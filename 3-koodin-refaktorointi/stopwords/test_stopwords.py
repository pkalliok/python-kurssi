
from stopwords import *

def test_finstops():
    assert 'okei' in fin_stops
    assert 'emme' not in fin_stops
    assert 'vai' in fin_stops

