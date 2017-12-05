"""
Create status column for TODOs
"""

from yoyo import step

__depends__ = {'20171201_01_9uNPC-create-todo-table'}

steps = [
    step("ALTER TABLE todo ADD COLUMN status TEXT DEFAULT 'new'",
        "ALTER TABLE todo DROP COLUMN status")
]
