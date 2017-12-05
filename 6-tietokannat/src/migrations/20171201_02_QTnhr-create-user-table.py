"""
Create user table
"""

from yoyo import step

__depends__ = {'20171201_01_9uNPC-create-todo-table'}

steps = [
    step("CREATE TABLE account(id SERIAL, username TEXT NOT NULL, password TEXT NOT NULL)",
        "DROP TABLE account")
]
