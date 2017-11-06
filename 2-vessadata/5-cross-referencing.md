Nyt kokeillaan yhdistää kahta aikasarjadataa.  Liitetään jokaiseen
vessanoven kiinni olemiseen tieto siitä, onko vessassa ollut liikettä
tuona aikana.

Ajanjaksojen ja ajanhetkien ristiinkorrelointi on mutkikasta.  Käytetään
siihen sortedcollections-kirjastoa.

```
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ pip install sortedcollections
```

SortedSet-tietorakenteella voi katsoa, onko kokoelmassa arvoja jollain
tietyllä välillä:

```
In [60]: from sortedcollections import SortedSet

In [61]: test = SortedSet([datetime(2017,1,22), datetime(2017,1,24), datetime(2017,2,12)])

In [62]: list(test.irange(datetime(2017,1,1), datetime(2017,2,1)))
Out[62]: [datetime.datetime(2017, 1, 22, 0, 0), datetime.datetime(2017, 1, 24, 0, 0)]
```

Tätä voidaan käyttää tekemään kokoelma niistä ajanhetkistä, jolloin on
tapahtunut liikkumista (`vessadata.py`):

```python
# [...]
from sortedcollections import SortedSet

# [...]

def movement_set(events):
    return SortedSet(time for time, place, evtype, value in events
            if evtype == 'movement' and value)

def timespan_has_movement(movement_set, start, end):
    return any(True for _ in movement_set.irange(start, end))

```

Ja kokeillaan:

```
In [65]: reload(vessadata)
Out[65]: <module 'vessadata' from '/home/atehwa/proj/esim-vessadata/vessadata.py'>

In [66]: ms = vessadata.movement_set(sensors[2,'movement'])

In [67]: vessadata.timespan_has_movement(ms, datetime(2016,6,8), datetime(2016,6,10))
Out[67]: True

In [68]: vessadata.timespan_has_movement(ms, datetime(2017,6,8), datetime(2017,6,10))
Out[68]: False
```

Käytetään tätä filtteröimään vain ne ajanjaksot, jolloin vessassa oli
liikettä (`vessadata.py`):

```python
def states_with_movement(states, movement_set):
    return ((start, end, place, closed)
        for start, end, place, evtype, closed in states
        if timespan_has_movement(movement_set, start, end))

```

Ja kokeillaan tämä:

```
In [78]: reload(vessadata)
Out[78]: <module 'vessadata' from '/home/atehwa/proj/esim-vessadata/vessadata.py'>

In [79]: vessadata.states_with_movement(vessadata.states_from_events(sensors[2,'closed']), ms)
Out[79]: <generator object states_with_movement.<locals>.<genexpr> at 0x7f2c68a92678>

In [80]: list(vessadata.states_with_movement(vessadata.states_from_events(sensors[2,'closed']), ms))[:3]
Out[80]: 
[(datetime.datetime(2016, 6, 4, 21, 34, 12),
  datetime.datetime(2016, 6, 4, 21, 48, 16),
  2,
  True),
 (datetime.datetime(2016, 6, 4, 21, 48, 17),
  datetime.datetime(2016, 6, 4, 22, 23, 9),
  2,
  False),
 (datetime.datetime(2016, 6, 4, 22, 23, 10),
  datetime.datetime(2016, 6, 4, 22, 23, 26),
  2,
  True)]

```

Ja taas työn tulokset talteen:

```
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ git add -p
diff --git a/vessadata.py b/vessadata.py
index 53a3229..5bea42b 100644
--- a/vessadata.py
+++ b/vessadata.py
@@ -2,6 +2,7 @@
 import csv
 from dateutil.parser import parse
 from itertools import islice, tee, groupby
+from sortedcollections import SortedSet
 
 def load_csv(filename):
     return csv.reader(open(filename))
Stage this hunk [y,n,q,a,d,/,j,J,g,e,?]? y
@@ -32,3 +33,15 @@ def states_from_events(events):
 def sensor_states(events):
     return map_values(states_from_events,
dict(by_place_and_type(events)))
 
+def movement_set(events):
+    return SortedSet(time for time, place, evtype, value in events
+            if evtype == 'movement' and value)
+
+def timespan_has_movement(movement_set, start, end):
+    return any(True for _ in movement_set.irange(start, end))
+
+def states_with_movement(states, movement_set):
+    return ((start, end, place, closed)
+        for start, end, place, evtype, closed in states
+        if timespan_has_movement(movement_set, start, end))
+
Stage this hunk [y,n,q,a,d,/,K,g,e,?]? y
<stdin>:28: new blank line at EOF.
+
warning: 1 line adds whitespace errors.

(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ git commit -m "Correlating movement data"
[master bf9dae9] Correlating movement data
 1 file changed, 13 insertions(+)

```

Tässä vaiheessa voisi laittaa talteen myös asennukset jälleen:


```
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ pip freeze > requirements.txt 
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ git add requirements.txt 
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ git commit -m "update reqs"
[master ac2e20f] update reqs
 1 file changed, 7 insertions(+)
```

