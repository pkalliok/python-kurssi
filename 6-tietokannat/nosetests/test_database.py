
from src.database import connection, migrations

def test_connection():
    assert hasattr(connection, 'cursor')
    cu = connection.cursor()
    cu.execute('select 1+2')
    assert cu.fetchall() == [(3,)]

def test_test_query():
    assert migrations.test_db_connection() == [(5,)]

