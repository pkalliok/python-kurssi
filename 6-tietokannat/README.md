# Dealing with databases in Python

Certainly no lack of options!  You can:

 1. Run the queries from your Python code
 2. Put your queries in separate files and load them (`pyesql` used
    here)
 3. Define your data model in SQLAlchemy and use that over SQL
 4. Use data structure specific wrappers such as pandas'
    `read_sql_query` and `to_sql` (used here)
 5. Use some magical stuff like `db.py`.

For migrating database schemas, there are also a few options:

 1. Use your web framework's migration tools, such as `flask_migrate` or
    Django's built-in migrations
 2. Use some specific migration library such as `alembic` (for
    SQLAlchemy) or `yoyo-migrations` (we use yoyo-migrations)

## Normal pyesql usage

Take a look at [./src/sql/queries.sql] and [./src/database.py].

```
In [1]: from src import database

In [2]: database.migrate()

In [3]: with database.connection: database.queries.new_todo(todo="hyvin menee")

In [4]: database.queries.all_todos()
Out[4]: 
[('foobar',),
 ('foo',),
 ('foo',),
 ('yay',),
 ('jotain',),
 ('jotain muuta',),
 ('jotain ihan muuta',),
 ('New todo item (90473)',),
 ('New todo item (64179)',),
 ('hyvin menee',)]

In [5]: from pandas import DataFrame as DF

In [6]: DF(database.queries.all_todos(), columns=["TODO"])
Out[6]: 
                    TODO
0                 foobar
1                    foo
2                    foo
3                    yay
4                 jotain
5           jotain muuta
6      jotain ihan muuta
7  New todo item (90473)
8  New todo item (64179)
9            hyvin menee

In [7]: from imp import reload

In [8]: reload(database)
Out[8]: <module 'src.database' from '/home/atehwa/proj/python-kurssi/6-tietokannat/src/database.py'>

In [9]: database.queries.newest_todo()
Out[9]: [('New todo item (36226)', datetime.datetime(2017, 12, 1, 11, 46, 22, 330737))]
```

