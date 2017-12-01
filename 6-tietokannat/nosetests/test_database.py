
from src.database import connection, queries, migrate, transactional
from random import randint

def test_connection():
    assert hasattr(connection, 'cursor')
    cu = connection.cursor()
    cu.execute('select 1+2')
    assert cu.fetchall() == [(3,)]

def test_test_query():
    assert queries.test_db_connection() == [(5,)]

def test_migration_creates_todos():
    migrate()
    assert isinstance(queries.all_todos(), list)

@transactional
def test_todo_add():
    migrate()
    todo = "New todo item (%d)" % randint(0,99999)
    [(id,)] = queries.new_todo(todo=todo)
    assert isinstance(id, int)
    assert (todo,) in queries.all_todos()

