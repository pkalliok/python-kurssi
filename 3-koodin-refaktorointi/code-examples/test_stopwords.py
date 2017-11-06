
from stopwords import *

def test_finstops():
    assert 'okei' in fin_stops
    assert 'emme' not in fin_stops
    assert 'vai' in fin_stops

def test_swestops():
    assert 'min' not in swe_stops
    assert 'och' in swe_stops

def test_engstops():
    assert 'me' not in en_stops
    assert 'the' in en_stops

def test_email_stops():
    assert 'kello' in email_stops
    assert 'madam' not in email_stops

def test_final_stops():
    assert 'okei' in final_stops
    assert 'emme' not in final_stops
    assert 'vai' in final_stops
    assert 'kello' in final_stops
    assert 'madam' not in final_stops

