
from src.database import connection

def test_connection():
    assert hasattr(connection, 'cursor')
    cu = connection.cursor()
    cu.execute('select 1+2')
    assert cu.fetchall() == [(3,)]

