
from os import environ
from os.path import dirname, join
import psycopg2, pyesql

basedir = dirname(__file__)

def sql_file(name):
    return join(basedir, "sql", "%s.sql" % name)

def new_conn():
    env = environ.get
    conn_params = dict(
            host=env('PGHOST', 'localhost'),
            port=env('PGPORT', '15432'),
            user=env('PGUSER', 'pydb'),
            database=env('PGDATABASE', 'pydb'),
            password=env('PGPASSWORD', 'hubbabubba'))
    return psycopg2.connect(**conn_params)

connection = new_conn()

def define_queries(name):
    return pyesql.parse_file(sql_file(name), name=name.title())(connection)

migrations = define_queries("migrations")
#queries = pyesql.parse_file(sql_file("queries"))
