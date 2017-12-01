
from os import environ
from os.path import dirname, join
from yoyo import read_migrations, get_backend
import psycopg2, pyesql

basedir = dirname(__file__)

def sql_file(name):
    return join(basedir, "sql", "%s.sql" % name)

def conn_params():
    env = environ.get
    return dict(
            host=env('PGHOST', 'localhost'),
            port=env('PGPORT', '15432'),
            user=env('PGUSER', 'pydb'),
            database=env('PGDATABASE', 'pydb'),
            password=env('PGPASSWORD', 'hubbabubba'))

connection = psycopg2.connect(**conn_params())

def conn_url():
    return "postgres://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" \
            % conn_params()

def migrate():
    backend = get_backend(conn_url())
    migrations = read_migrations(join(basedir, "migrations"))
    backend.apply_migrations(backend.to_apply(migrations))

def define_queries(name):
    return pyesql.parse_file(sql_file(name), name=name.title())(connection)

queries = define_queries("queries")

