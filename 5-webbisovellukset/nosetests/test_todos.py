#!/usr/bin/env python3

from requests import get, post
from random import randint

def test_todo():
    resp = get("http://localhost:3000/api/v1/todo").json()
    assert isinstance(resp, list)

def test_todo_add():
    todo = "Todo list item %d: murder (soft)" % randint(0, 9999)
    resp = post("http://localhost:3000/api/v1/todo", json=todo)
    assert resp.status_code == 201
    assert resp.json() == "ok"
    assert todo in get("http://localhost:3000/api/v1/todo").json()

