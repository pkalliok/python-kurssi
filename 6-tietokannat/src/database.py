
from os import environ
import psycopg2

conn_params = dict(
        host=environ.get('PGHOST', 'localhost'),
        port=environ.get('PGPORT', '15432'),
        user=environ.get('PGUSER', 'pydb'),
        database=environ.get('PGDATABASE', 'pydb'),
        password=environ.get('PGPASSWORD', 'hubbabubba'))

connection = psycopg2.connect(**conn_params)

