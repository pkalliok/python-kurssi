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

Usein, jos kokonainen funktio on wrapattu with:-blokkiin, kannattaa
wrappausta varten tehdä koristerija.  Eli aasinsillan kautta:

## Koristelijat (dekoraattorit)

Koristelijat "muuntavat" määriteltävää funktiota haluamallaan tavalla.
Nämä kaksi tarkoittavat suunnilleen samaa:

```python
@koristele
def mun_funktio(x): return jotain(x)
```

ja

```python
def mun_funktio(x): return jotain(x)
mun_funktio = koristele(mun_funktio)
```

## `yield` ja generaattorifunktiot

Generaattorifunktiot ovat keskeytettäviä suorituskonteksteja.  Tämä on
tosi monipuolinen ohjelmointitekniikka, jolla voi toteuttaa korutiineja,
asynkronisia ohjelmia ja vaikkapa kontekstinkäsittelijöitä.
