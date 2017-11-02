Kokeillaan vähän `ipython`-tulkissa, miten CSV-tuki toimii:

```
In [1]: import csv

In [2]: ?csv.reader
Docstring:
csv_reader = reader(iterable [, dialect='excel']
                        [optional keyword args])
    for row in csv_reader:
        process(row)

The "iterable" argument can be any object that returns a line
of input for each iteration, such as a file object or a list.  The
optional "dialect" parameter is discussed below.  The function
also accepts optional keyword arguments which override settings
provided by the dialect.

The returned object is an iterator.  Each iteration returns a row
of the CSV file (which can span multiple input lines).
Type:      builtin_function_or_method

In [3]: open('toilets.csv')
Out[3]: <_io.TextIOWrapper name='toilets.csv' mode='r' encoding='UTF-8'>

In [4]: open('toilets.csv').__next__()
Out[4]: 'place_id,value,time,type,id,device_id\n'

In [5]: csv.reader(open('toilets.csv'))
Out[5]: <_csv.reader at 0x7fcb7a5eff98>

In [6]: csv.reader(open('toilets.csv')).__next__()
Out[6]: ['place_id', 'value', 'time', 'type', 'id', 'device_id']
```

Kirjoitetaan editorilla tiedostoon `vessadata.py`:

```python
import csv

def load_csv(filename): 
    return csv.reader(open(filename))

```

Ladataan ja kokeillaan:

```
In [7]: import vessadata

In [8]: vessadata.load_csv('toilets.csv')
Out[8]: <_csv.reader at 0x7fcb7a5efc18>

In [9]: vessadata.load_csv('toilets.csv').__next__()
Out[9]: ['place_id', 'value', 'time', 'type', 'id', 'device_id']
```

Asennetaan dateutil, jolla voi kätevästi jäsentää päivämääriä:

```bash
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ pip install python-dateutil
Collecting python-dateutil
  Using cached python_dateutil-2.6.1-py2.py3-none-any.whl
Requirement already satisfied: six>=1.5 in ./myenv/lib/python3.5/site-packages (from python-dateutil)
Installing collected packages: python-dateutil
Successfully installed python-dateutil-2.6.1
```

Kokeillaan:

```
In [4]: from dateutil.parser import parse

In [5]: parse('2017-02-15T13:40')
Out[5]: datetime.datetime(2017, 2, 15, 13, 40)
```

Lisää määrittelyitä `vessadata.py`-tiedostoon:

```python
import csv
from dateutil.parser import parse
from itertools import islice

def load_csv(filename):
    return csv.reader(open(filename))

def parsed_vessadata(csv_data):
    return ((parse(time), int(place), evtype, bool(value))
            for place, value, time, evtype, _, _ in islice(csv_data, 1, None))

```

Kokeillaan:

```
In [8]: from imp import reload

In [9]: reload(vessadata)
Out[9]: <module 'vessadata' from '/home/atehwa/proj/esim-vessadata/vessadata.py'>

In [10]: next(vessadata.parsed_vessadata(vessadata.load_csv('toilets.csv')))
Out[10]: (datetime.datetime(2016, 6, 14, 5, 36, 49), 2, 'movement', True)
```

