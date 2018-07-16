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
    SQLAlchemy), `sqlturk` or `yoyo-migrations` (we use yoyo-migrations)
 3. Automatically generate schema changes from changes in code
    (`alembic` and `sql-schema-builder` can do this)

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

## Handling data with Pandas

Pandas has its own support for reading various sources of data:

```
In [19]: import pandas as pd

In [20]: events = pd.read_csv('toilets.csv', index_col=['id'], parse_dates=['tim
    ...: e'], dtype=dict(place_id=int, device_id=int, value=float))

In [21]: events.head()
Out[21]: 
       place_id  value                time      type  device_id
id                                                             
47890         2    0.0 2016-06-14 05:36:49  movement    1210115
47891         2    1.0 2016-06-14 05:47:18  movement    1210115
47892         2    1.0 2016-06-14 05:47:23  movement    1210115
47893         2    1.0 2016-06-14 05:47:24  movement    1210115
47894         2    1.0 2016-06-14 05:47:28  movement    1210115

In [22]: events.time.max()
Out[22]: Timestamp('2016-06-20 15:01:03')

In [23]: events.time.min()
Out[23]: Timestamp('2016-06-04 20:26:16')

In [27]: todos = pd.read_sql_query('select * from todo', database.connection, in
    ...: dex_col=['id'])

In [28]: todos.head()
Out[28]: 
      todo                         ts
id                                   
1   foobar 2017-12-01 11:00:05.884024
2      foo 2017-12-01 11:00:05.884024
3      foo 2017-12-01 11:00:05.884024
4      yay 2017-12-01 11:05:34.118534
5   jotain 2017-12-01 11:14:42.420348
```

Pandas tries to make a sensible "relation algebra".

```
In [32]: todos.ts
Out[32]: 
id
1    2017-12-01 11:00:05.884024
2    2017-12-01 11:00:05.884024
3    2017-12-01 11:00:05.884024
4    2017-12-01 11:05:34.118534
5    2017-12-01 11:14:42.420348
6    2017-12-01 11:14:42.420348
7    2017-12-01 11:14:42.420348
9    2017-12-01 11:22:58.112745
10   2017-12-01 11:39:31.936157
11   2017-12-01 11:41:49.884183
12   2017-12-01 11:44:42.988026
13   2017-12-01 11:46:22.296877
14   2017-12-01 11:46:22.330737
Name: ts, dtype: datetime64[ns]

In [33]: todos.ts > datetime(2017,12,1,11,14)
Out[33]: 
id
1     False
2     False
3     False
4     False
5      True
6      True
7      True
9      True
10     True
11     True
12     True
13     True
14     True
Name: ts, dtype: bool

In [34]: todos[todos.ts > datetime(2017,12,1,11,14)]
Out[34]: 
                         todo                         ts
id                                                      
5                      jotain 2017-12-01 11:14:42.420348
6                jotain muuta 2017-12-01 11:14:42.420348
7           jotain ihan muuta 2017-12-01 11:14:42.420348
9       New todo item (90473) 2017-12-01 11:22:58.112745
10      New todo item (64179) 2017-12-01 11:39:31.936157
11                hyvin menee 2017-12-01 11:41:49.884183
12      New todo item (87908) 2017-12-01 11:44:42.988026
13  Another todo item (54389) 2017-12-01 11:46:22.296877
14      New todo item (36226) 2017-12-01 11:46:22.330737

In [35]: todos[todos.ts > datetime(2017,12,1,11,14)].todo
Out[35]: 
id
5                        jotain
6                  jotain muuta
7             jotain ihan muuta
9         New todo item (90473)
10        New todo item (64179)
11                  hyvin menee
12        New todo item (87908)
13    Another todo item (54389)
14        New todo item (36226)
Name: todo, dtype: object
```

