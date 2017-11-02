## Vessadataesimerkin pointti

Isojen datamassojen käsittely koostuu pienistä askelista.  Yksi hyöty
funktionaalisten kirjastojen, kielten ja koodin tutkimisesta on se, että
oppii tietämään, mitä nuo pienet askeleet ovat.

Näytän, miten näillä pienillä askelilla saadaan data pikku hiljaa
haluttuun muotoon.

## Listat vs iteraattorit

Python3:ssa aika monet sisäänrakennetut funktiot (range, zip, map, ...)
tuottavat iteraattoreita.  Iteraattorit ovat listan kaltaisia juttuja,
joita voi käydä läpi.  Ne muodostavat halutut arvot laiskasti tarpeen
mukaan, joten ne eivät kuluta muistia.

Mutta iteraattoreissa on erittäin iso miinus: niiden lukeminen on
sivuvaikutuksellista.  Sen vuoksi samaa iteraattoria ei kannata antaa
syötteeksi kahdelle funktiolle / rakenteelle, koska tyypillisesti toinen
niistä kuluttaa iteraattorin arvot eikä toiselle jää mitään.
Iteraattoreiden sisällön tarkastelu REPL:ssä on myös ongelmallista,
koska varsinaisten arvojen hakeminen iteraattorista kuluttaisi ne.

Aina voi muuttaa iteraattorit listoiksi.  Niitä voi lukea niin monta
kertaa kuin haluaa.  Ne tietysti kuluttavat muistia minkä kuluttavat.

Jos iteraattorin sisällön tarvitsee useampaan käyttöön muttei halua
kuluttaa muistia, voi käyttää itertools.tee()-funktiota.

