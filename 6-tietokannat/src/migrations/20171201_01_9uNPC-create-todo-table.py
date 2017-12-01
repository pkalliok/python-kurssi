"""
Create TODO table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        "CREATE TABLE todo (id SERIAL, todo TEXT, ts TIMESTAMP DEFAULT now())",
        "DROP TABLE todo"
        )
]
