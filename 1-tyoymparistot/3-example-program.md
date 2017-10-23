Uudessa päätteessä (tämä on vain testien tulosten näyttämistä varten):

```
[atehwa@undantag ~]$ cd proj/esim-python/
[atehwa@undantag ~/proj/esim-python]$ . myenv/bin/activate
(myenv) [atehwa@undantag ~/proj/esim-python]$ nosy 

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
```

Kehityspäätteessä (saa käyttää mitä editoria huvittaa):

```
(myenv) [atehwa@undantag ~/proj/esim-python]$ vi test_wordcount.py 
(myenv) [atehwa@undantag ~/proj/esim-python]$ cat test_wordcount.py 

from wordcount import wordcount

def test_wordcount():
    assert wordcount("hei hei vaan") == dict(hei=2, vaan=1)

```

Testipääte näyttää:

```
E
======================================================================
ERROR: test_wordcount (nose2.loader.ModuleImportFailure)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_wordcount
Traceback (most recent call last):
  File "/home/atehwa/proj/esim-python/myenv/lib/python3.5/site-packages/nose2/plugins/loader/discovery.py", line 200, in _find_tests_in_file
    module = util.module_from_name(module_name)
  File "/home/atehwa/proj/esim-python/myenv/lib/python3.5/site-packages/nose2/util.py", line 90, in module_from_name
    __import__(name)
  File "/home/atehwa/proj/esim-python/test_wordcount.py", line 2, in <module>
    from wordcount import wordcount
ImportError: No module named 'wordcount'


----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)
```

Toteutetaan kehityspäätteessä wordcount:

```
(myenv) [atehwa@undantag ~/proj/esim-python]$ vi wordcount.py
(myenv) [atehwa@undantag ~/proj/esim-python]$ cat wordcount.py 

from itertools import groupby

def wordcount(str):
    return dict((word, len(list(occ)))
		for word, occ in groupby(str.split()))

```

Testipääte näyttää nyt:

```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

```

Viedään vielä talteen:

```
(myenv) [atehwa@undantag ~/proj/esim-python]$ git add test_wordcount.py wordcount.py 
(myenv) [atehwa@undantag ~/proj/esim-python]$ git commit -m "Programs"
[master f13d816] Programs
 2 files changed, 16 insertions(+)
 create mode 100644 test_wordcount.py
 create mode 100644 wordcount.py
```
