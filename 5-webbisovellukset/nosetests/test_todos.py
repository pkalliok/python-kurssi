#!/usr/bin/env python3

from requests import get, post
from random import randint
from os import environ

root = environ.get("SERVICE_ROOT", "http://localhost:3000")
endpoint = root + "/api/v1/todo"

def test_todo():
    resp = get(endpoint).json()
    assert isinstance(resp, list)

def test_todo_add():
    todo = "Todo list item %d: murder (soft)" % randint(0, 9999)
    resp = post(endpoint, json=todo)
    assert resp.status_code == 201
    assert resp.json() == "ok"
    assert todo in get(endpoint).json()

