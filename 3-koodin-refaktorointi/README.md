# Koodin refaktorointi

proseduuri:
 1. test runner pystyyn
 1. tehdään testit jos ne puuttuu
 1. fiksataan epäidiomaattiset kohdat
 1. poistetaan turhat sisennykset
 1. etsitään toisto ja poistetaan
 1. otetaan looppien sisässä olevat laskennat ja muutetaan ne funktioiksi
 1. pätkitään pitkät funktiot apumäärittelyiksi
 1. muutetaan kaikki imperatiiviset silmukat funktionaalisiksi
 1. poistetaan loput sivuvaikutukselliset asiat

## Esimerkki 1: tekstianalyysin apumäärittelyt

Lähtökohta:
 * https://github.com/pkalliok/python-kurssi/blob/806e0e9c909e4f22b5fb12d4df3bbe1b08966369/3-koodin-refaktorointi/stopwords/stopwords.py

Testien kirjoitusta:
 * https://github.com/pkalliok/python-kurssi/commit/be810aafdac64eb835b585ca343f1691c3af292a
 * https://github.com/pkalliok/python-kurssi/commit/77f3e992190743f6448444c98761cd3e62acb0ba
 * https://github.com/pkalliok/python-kurssi/commit/193b9cdfd236f87e120d250c95cfa416181a586d
 * https://github.com/pkalliok/python-kurssi/commit/cc69fa807e4a71169626cdd1034e67ea5311fae4

Epäidiomaattisuuksien korjausta:
 * https://github.com/pkalliok/python-kurssi/commit/6898576b2e7936b5c6e8a6c3a1ba67571c3c7475

Turhat imperatiiviset silmukat pois:
 * https://github.com/pkalliok/python-kurssi/commit/c04bee04d726e5a9f94f650b0b483554c2ff41ba

## Esimerkki 2: apuskripti .vcxproj-tiedostojen päivitykseen

Lähtökohta:
 * https://github.com/pkalliok/python-kurssi/blob/2105b61bf303d119d15dd8f9616ac883bb6ba2dc/3-koodin-refaktorointi/code-examples/dependency_updater.py

Dataa (fixtureja) testejä varten:
 * https://github.com/pkalliok/python-kurssi/tree/5d9a2036add4c7adc45e71a81135ab0205729b54/3-koodin-refaktorointi/code-examples/dependency_updater_test_data

Testien kirjoitusta:
 * https://github.com/pkalliok/python-kurssi/blob/5d9a2036add4c7adc45e71a81135ab0205729b54/3-koodin-refaktorointi/code-examples/test_dependency_updater.py
 * https://github.com/pkalliok/python-kurssi/commit/f8271a1c244ac38ce787d98a3f953e417a30e2d0
 * https://github.com/pkalliok/python-kurssi/commit/393b2f7758cfa00ee7b227e72cf74081919442e7
 * https://github.com/pkalliok/python-kurssi/commit/ce3c7dc4f6415cc062c6676b354b9104e36f76a2
 * https://github.com/pkalliok/python-kurssi/commit/4f89bc9d6b55e2268e4721f6df646a898bd3d2a6

