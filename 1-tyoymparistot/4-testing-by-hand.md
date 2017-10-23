Taas uudessa päätteessä (joka on tarkoitettu kokeilemiseen):

```
[atehwa@undantag ~]$ cd proj/esim-python/
[atehwa@undantag ~/proj/esim-python]$ . myenv/bin/activate
(myenv) [atehwa@undantag ~/proj/esim-python]$ python3
Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import imp, wordcount
>>> wordcount.wordcount('voi voi kun voi voi olla kallista')
{'kun': 1, 'voi': 2, 'kallista': 1, 'olla': 1}
```

Hmm bugi, lisätään testejä:

```
[atehwa@undantag ~]$ cd proj/esim-python/
[atehwa@undantag ~/proj/esim-python]$ . myenv/bin/activate
(myenv) [atehwa@undantag ~/proj/esim-python]$ python3
Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import imp, wordcount
>>> wordcount.wordcount('voi voi kun voi voi olla kallista')
{'kun': 1, 'voi': 2, 'kallista': 1, 'olla': 1}
```

Testien suorittaja näyttää:

```
F 
======================================================================
FAIL: test_wordcount.transplant_class.<locals>.C (test_wordcount)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/atehwa/proj/esim-python/test_wordcount.py", line 7, in test_wordcount
    dict(voi=4, kun=1, olla=1, kallista=1)
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

Korjataan toteutus:

```
(myenv) [atehwa@undantag ~/proj/esim-python]$ vi wordcount.py 
(myenv) [atehwa@undantag ~/proj/esim-python]$ cat wordcount.py 

from itertools import groupby

def wordcount(str):
    return dict((word, len(list(occ)))
            for word, occ in groupby(sorted(str.split())))

```

Nyt testien suorittaja näyttää:

```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Kokeilupäätteessä, jossa pyörii REPL, vanha määrittely on voimassa
reloadiin asti:

```python
>>> wordcount.wordcount('voi voi kun voi voi olla kallista')
{'kun': 1, 'voi': 2, 'kallista': 1, 'olla': 1}
>>> imp.reload(wordcount)
<module 'wordcount' from '/home/atehwa/proj/esim-python/wordcount.py'>
>>> wordcount.wordcount('voi voi kun voi voi olla kallista')
{'kun': 1, 'voi': 4, 'kallista': 1, 'olla': 1}
```

