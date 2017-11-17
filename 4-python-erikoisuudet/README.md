# Pythonin erikoisuudet

Tällä kerralla käydään läpi joitain rakenteita, jotka ovat idiomaattisia
Pythonissa, mutta eivät tyypillisiä (ainakaan kaikissa) muissa kielissä.

Yleensä Python ei ole ollut pioneeri missään, vaan on lainannut muista
kielistä näitä ideoita.  Lähinnä on nähty paljon vaivaa siihen, että
ominaisuudet olisivat "nättejä" ja sopisivat Pythonin muihin
ominaisuuksiin.

## Generaattorit ja perustietorakenteiden algebra

Tätä on käsitelty jo, mutta muutamia linkkejä:

 * Listakeräelmät: https://www.python.org/dev/peps/pep-0202/
 * Generaattorilauseet: https://www.python.org/dev/peps/pep-0289/
 * Iteraattorialgebra:
   https://docs.python.org/3/library/itertools.html#itertools-recipes
 * Funktionaalisia apuja:
   https://docs.python.org/3/library/functools.html ja erityisesti
   lisäkirjasto https://github.com/Suor/funcy

Iteraattoreita voi luoda kolmella tavalla:

 * Oliona:
   https://docs.python.org/3/library/stdtypes.html#iterator-types
 * Generaattorifunktiona: https://www.python.org/dev/peps/pep-0255/
   (tähän palataan myöhemmin)
 * Generaattorilauseena.

Iteraattoreilla voi tehdä potentiaalisesti äärettömiä kokoelmia:

```python
from itertools import *
list(islice(cycle([1,2,3]), 10))
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1]
```

Äärettömästä kokoelmasta voi tuottaa toisen äärettömän kokoelman:

```python
list(islice((el+7 for el in cycle([1,2,3]) if el%2), 10))
[8, 10, 8, 10, 8, 10, 8, 10, 8, 10]
```

## `with` ja kontekstinkäsittelijät

Tämä tuli jo vastaan testifixtureissa.  Kontekstinkäsittelijät on
tarkoitettu asioihin, joissa on tärkeää tietää, milloin tiettyä oliota
(resurssia, tms) lakataan käyttämästä.

 * alkuperäinen määrittely: https://www.python.org/dev/peps/pep-0343/
 * erilaisia avuliaiksi tarkoitettuja kontekstinkäsittelijöitä:
   https://docs.python.org/3/library/contextlib.html

Tietokannat, niiden transaktiot ja kursorit ovat yleensä
kontekstinkäsittelijöitä (toteuttavat kontekstiprotokollan).

 * Postgresille: http://initd.org/psycopg/docs/usage.html#with-statement
 * MySQL:lle:
   https://pythonhosted.org/oursql/api.html#cursor-context-manager
 * SQLitelle:
   https://docs.python.org/3/library/sqlite3.html#using-the-connection-as-a-context-manager

Usein, jos kokonainen funktio on wrapattu `with`-blokkiin, kannattaa
wrappausta varten tehdä koristerija.  Eli aasinsillan kautta:

## Koristelijat (dekoraattorit)

Koristelijat "muuntavat" määriteltävää funktiota haluamallaan tavalla.
Nämä kaksi tarkoittavat suunnilleen samaa:

```python
@koristele(argumentti)
def mun_funktio(x): return jotain(x)
```

ja

```python
def mun_funktio(x): return jotain(x)
mun_funktio = koristele(argumentti)(mun_funktio)
```

Mitä koristelija voi tehdä?  Ainakin:

 * Estää `mun_funktio`:n kutsumisen jossain tilanteessa
 * Kutsua `mun_funktio`:ta monta kertaa
 * Muutella `mun_funktio`:n argumentteja
 * Tehdä jotain (esim. lokitusta, resurssinvarauksia, ...) ennen ja
   jälkeen `mun_funktio`:n kutsujen
 * Merkitä jotain muistiin heti määrittelyvaiheessa

Lisää tietoa:

 * määrittely: https://www.python.org/dev/peps/pep-0318/
 * http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html
 * Aivan sikana esimerkkikäyttötapauksia:
   https://stackoverflow.com/questions/489720/what-are-some-common-uses-for-python-decorators
 * Flask-kirjasto käyttää runsaasti dekoraattoreita antamaan
   lisämäärityksiä (ja osoitteita) erilaisten HTTP-kutsujen
   käsittelijöille:
   http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/

## `yield` ja generaattorifunktiot

Generaattorifunktiot ovat keskeytettäviä suorituskonteksteja.  Tämä on
tosi monipuolinen ohjelmointitekniikka, jolla voi toteuttaa korutiineja,
asynkronisia ohjelmia ja vaikkapa kontekstinkäsittelijöitä.  Jos
"korutiini" ei ole tuttu sana, niin se on ... yleistys siitä mitä
vaikkapa Clojuren transduktorit tai Unixin putket pyrkivät tekemään :)

Generaattorifunktioilla voi tehdä asioita, jotka ovat epäluontevia
generaattorilauseilla:

```python
def fibonacci_seq():
    x, y = 1, 1
    while True:
        yield x
        x, y = y, x+y

list(islice(fibonacci_seq(), 10))
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

```

Joskus saman saa tosin aikaan pahalla kikkailulla:

```python
list(islice((a for a, b in
  accumulate(cycle([(1,1)]), lambda x, _: (x[1], x[0]+x[1]))),
  10))
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

Generaattorifunktiot voivat olla rekursiivisia:

```python
def numbers_from(x):
    yield x
    yield from numbers_from(x+1)

list(islice(numbers_from(1), 5))
[1, 2, 3, 4, 5]
```

Sillä voi tehdä asioita, jotka ovat vaan tosi vaikeita
generaattorilauseilla:

```python
def bifurcate(num):
    if num < 0: return
    yield from bifurcate(num-1)
    yield num
    yield from bifurcate(num-1)

list(bifurcate(3))
[0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0]
```

Taikka vaikka rekursiivisen Erastotheneen seulan:

```python
def sieve(nums):
    p = next(nums)
    yield p
    yield from sieve(n for n in nums if n%p)
    
list(islice(sieve(count(2)), 10))
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

Olennaista on, että generaattoreiden on helppoa kutsua toisiaan.

```python
def insane_processing_step(coll):
    acc = 15
    for num in coll:
        acc = int((num - acc) * .75)
        yield acc

list(islice(insane_processing_step(count(0)), 15))
[-11, 9, -5, 6, -1, 4, 1, 4, 3, 4, 4, 5, 5, 6, 6]
```

## Asynkroninen ohjelmointi

Koska generaattorit pystyvät keskeyttämään koodin suorituksen tiettyyn
pisteeseen (`yield`) ja jatkamaan siitä pyydettäessä, niitä käytetään
myös asynkronisessa ohjelmoinnissa kertomaan, että ohjelma haluaa
odotella jotain ja on aika tehdä välillä jotain muuta.  Mutta viime
aikoina Pythonissa on asteittain rakennettu erillinen tuki
asynkroniselle ohjelmoinnille ja generaattoreita yritetään kovasti
eriyttää asynkronisista korutiineista.

Esimerkkejä nykyaikaisesta asynkronisesta Python-ohjelmoinnista löytyy
vaikkapa täältä: https://aiohttp.readthedocs.io/en/stable/

