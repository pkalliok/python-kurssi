#!/usr/bin/env python3

from requests import get
from os import environ

root = environ.get("SERVICE_ROOT", "http://localhost:3000")

def test_hello():
    assert get("%s/hello" % root).text \
            == "Dead kittens and suffering"

def test_ping():
    assert "pong" in get("%s/ping" % root).text

def test_nonexistent():
    assert get("%s/nonexistent" % root).status_code == 404

def test_root_redirect():
    resp = get(root)
    assert resp.history[0].status_code == 302
    assert 'kittens' in resp.text

