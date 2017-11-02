Nyt on tavoitteena tuottaa raa'asta tapahtumadatasta rakenteellisempaa
dataa: ensimmäiseksi voitaisiin tuottaa esimerkiksi ajanjaksoja, jolloin
ovet ovat olleet auki/kiinni.

Ryhmitellään aineisto sensoreittain (`vessadata.py`):

```python
import csv
from dateutil.parser import parse
from itertools import islice, groupby

def load_csv(filename):
    return csv.reader(open(filename))

def parsed_vessadata(csv_data):
    return ((parse(time), int(place), evtype, bool(float(value)))
            for place, value, time, evtype, _, _ in islice(csv_data, 1, None))

def place_and_type(event): return event[1:3]

def by_place_and_type(events):
    return groupby(sorted(events, key=place_and_type), place_and_type)

```

Kokeillaan:

```
In [19]: reload(vessadata)
Out[19]: <module 'vessadata' from '/home/atehwa/proj/esim-vessadata/vessadata.py'>

In [20]: vessadata.place_and_type(next(vessadata.parsed_vessadata(vessadata.load
    ...: _csv('toilets.csv'))))
Out[20]: (2, 'movement')

In [21]: dict(vessadata.by_place_and_type(vessadata.parsed_vessadata(vessadata.l
    ...: oad_csv('toilets.csv'))))
Out[21]: 
{(2, 'closed'): <itertools._grouper at 0x7ff5fde0f438>,
 (2, 'movement'): <itertools._grouper at 0x7ff5fde0f208>,
 (3, 'closed'): <itertools._grouper at 0x7ff5fde0f320>,
 (3, 'movement'): <itertools._grouper at 0x7ff5fde0f4e0>,
 (4, 'closed'): <itertools._grouper at 0x7ff5fde0f4a8>,
 (4, 'movement'): <itertools._grouper at 0x7ff5fde0f470>,
 (5, 'closed'): <itertools._grouper at 0x7ff5fd3ace48>,
 (5, 'movement'): <itertools._grouper at 0x7ff5fd3cada0>,
 (5, 'occupied'): <itertools._grouper at 0x7ff5fd3caf28>}
```

Nyt meillä on siis jokaisen sensorin tapahtumadata omana
iteraattorinaan.  Seuraavaksi muunnetaan ne aikavälidataksi, mutta
määritellään sitä varten pari apufunktiota, joita tarvitaan aika usein.
`vessadata.py`:

```python
# [...]
from itertools import islice, tee, groupby

# [...]

def pairs(seq):
    s1, s2 = tee(seq)
    return zip(s1, islice(s2, 1, None))

def map_values(f, dictionary):
    return {key: f(val) for key, val in dictionary.items()}

```

Ja kokeillaan:

```
In [25]: reload(vessadata)
Out[25]: <module 'vessadata' from '/home/atehwa/proj/esim-vessadata/vessadata.py'>

In [26]: list(vessadata.pairs([5,3,2,"foo",0]))
Out[26]: [(5, 3), (3, 2), (2, 'foo'), ('foo', 0)]

In [27]: vessadata.map_values(lambda x: x+x, dict(foo=3, bar=4))
Out[27]: {'bar': 8, 'foo': 6}

```

Sitten varsinainen koodi aikavälidatamuunnokselle (`vessadata.py`):

```python
def states_from_events(events):
    by_time = lambda event: event[0]
    consecutive_events = pairs(sorted(events, key=by_time))
    return ((start_time, end_time, place, evtype, value) 
            for (start_time, place, evtype, value), (end_time, _, _, _)
            in consecutive_events)

```

Ja testataan:

```
In [39]: reload(vessadata)
Out[39]: <module 'vessadata' from '/home/atehwa/proj/esim-vessadata/vessadata.py'>

In [40]: sensor1 = next(vessadata.by_place_and_type(vessadata.parsed_vessadata(v
    ...: essadata.load_csv('toilets.csv'))))

In [41]: s1_events = list(sensor1[1])

In [42]: s1_events[:5]
Out[42]: 
[(datetime.datetime(2016, 6, 14, 5, 47, 11), 2, 'closed', False),
 (datetime.datetime(2016, 6, 14, 5, 47, 14), 2, 'closed', True),
 (datetime.datetime(2016, 6, 14, 5, 51, 54), 2, 'closed', False),
 (datetime.datetime(2016, 6, 14, 5, 51, 57), 2, 'closed', True),
 (datetime.datetime(2016, 6, 14, 7, 22, 42), 2, 'closed', False)]

In [43]: list(islice(vessadata.states_from_events(s1_events),5))
Out[43]: 
[(datetime.datetime(2016, 6, 4, 20, 35, 53),
  datetime.datetime(2016, 6, 4, 20, 35, 56),
  2,
  'closed',
  False),
 (datetime.datetime(2016, 6, 4, 20, 35, 56),
  datetime.datetime(2016, 6, 4, 20, 35, 59),
  2,
# [...]
```

Nyt voidaan tehdä vastaava tiladata kaikista sensoreista
(`vessadata.py`):

```python
def sensor_states(events):
    return map_values(states_from_events, dict(by_place_and_type(events)))

```

Ja kokeillaan:

```python
In [44]: reload(vessadata)
Out[44]: <module 'vessadata' from '/home/atehwa/proj/esim-vessadata/vessadata.py'>

In [45]: vessadata.sensor_states(vessadata.parsed_vessadata(vessadata.load_csv('
    ...: toilets.csv')))
Out[45]: 
{(2, 'closed'): <generator object states_from_events.<locals>.<genexpr> at 0x7ff5feb18728>,
 (2, 'movement'): <generator object states_from_events.<locals>.<genexpr> at 0x7ff5feb43410>,
 (3, 'closed'): <generator object states_from_events.<locals>.<genexpr> at 0x7ff5fd582728>,
 (3, 'movement'): <generator object states_from_events.<locals>.<genexpr> at 0x7ff5feabaa98>,
 (4, 'closed'): <generator object states_from_events.<locals>.<genexpr> at 0x7ff5fd582d58>,
 (4, 'movement'): <generator object states_from_events.<locals>.<genexpr> at 0x7ff5feabad00>,
 (5, 'closed'): <generator object states_from_events.<locals>.<genexpr> at 0x7ff5fd582c50>,
 (5, 'movement'): <generator object states_from_events.<locals>.<genexpr> at 0x7ff5fd582db0>,
 (5, 'occupied'): <generator object states_from_events.<locals>.<genexpr> at 0x7ff5fdde5308>}

```

Työskentelyn tulokset talteen:

```
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ pip freeze > requirements.txt
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ git add Makefile vessadata.py requirements.txt 
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ git commit -m "Vessadata handling"
[master (root-commit) 97b26e7] Vessadata handling
 3 files changed, 55 insertions(+)
 create mode 100644 Makefile
 create mode 100644 requirements.txt
 create mode 100644 vessadata.py
```

