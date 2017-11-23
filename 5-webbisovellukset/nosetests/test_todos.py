#!/usr/bin/env python3

from requests import get, post

def test_todo():
    resp = get("http://localhost:3000/api/v1/todo").json()
    assert isinstance(resp, list)

