#!/usr/bin/env python3

from requests import get

def test_hello():
    assert get("http://localhost:3000/hello").text \
            == "Dead kittens and suffering"

