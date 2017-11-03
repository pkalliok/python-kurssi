Ensin laitetaan tieto helposti leikittävään muotoon (listoiksi):

```
In [31]: d = list(vessadata.parsed_vessadata(vessadata.load_csv('toilets.csv')))

In [32]: sensors = {k: list(val) for k, val in vessadata.by_place_and_type(d)}

In [33]: vessadata.map_values(len, sensors)
Out[33]: 
{(2, 'closed'): 4904,
 (2, 'movement'): 28222,
 (3, 'closed'): 1510,
 (3, 'movement'): 4423,
 (4, 'closed'): 2564,
 (4, 'movement'): 3826,
 (5, 'closed'): 3326,
 (5, 'movement'): 9672,
 (5, 'occupied'): 1}
```

Sitten töihin.  Asennetaan matplotlib:

```
(myenv) [atehwa@undantag ~/proj/esim-vessadata]$ pip install matplotlib
```

Kokeillaan (plotin pitäisi näkyä myös erillisessä ikkunassa):

```
In [67]: from matplotlib import pyplot

In [68]: %matplotlib
Using matplotlib backend: TkAgg

In [69]: pyplot.plot([1,3,4,2,5])
Out[69]: [<matplotlib.lines.Line2D at 0x7ff5e302c3c8>]

In [70]: pyplot.close()

In [71]: pyplot.broken_barh([(0,10),(16,3),(40,15)], (0,2))
Out[71]: <matplotlib.collections.BrokenBarHCollection at 0x7ff5e323c470>
```

Sitten tehdään muutamia vessadatan näyttämisen apumäärittelyitä
tiedostoon `ts_plot.py`:

```python
from matplotlib import pyplot, dates

d = dates.date2num

def states_for_pyplot(states):
    return [(d(start), d(end) - d(start))
            for start, end, _, _, value in states
            if value]

def add_states_to_plot(plot, y, states):
    plot.broken_barh(states_for_pyplot(states), (y, 1))
    plot.xaxis_date()

```

Ja kokeillaan:

```
In [126]: import ts_plot

In [127]: fig, ax = pyplot.subplots()

In [128]: ts_plot.add_states_to_plot(ax, 1, vessadata.states_from_events(sensors[2,'closed']))
```

