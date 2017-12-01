
from src.database import connection, queries, migrate

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

