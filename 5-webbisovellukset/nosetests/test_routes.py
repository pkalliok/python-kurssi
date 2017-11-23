#!/usr/bin/env python3

from requests import get

def test_hello():
    assert get("http://localhost:3000/hello").text \
            == "Dead kittens and suffering"

def test_ping():
    assert "pong" in get("http://localhost:3000/ping").text

def test_nonexistent():
    assert get("http://localhost:3000/nonexistent").status_code == 404

def test_root_redirect():
    resp = get("http://localhost:3000/")
    assert resp.history[0].status_code == 302
    assert 'kittens' in resp.text

