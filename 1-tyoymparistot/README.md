## Kirjastojen asennustapojen vertailua

  1. käyttöjärjestelmän paketointivälineillä
    * - ei tarkkaa hallintaa versioihin
    * + automaattiset tietoturvapäivitykset

  2. pip:llä (tai easy_installilla) järjestelmänlaajuisesti
    * - rikkoutuu, kun järjestelmää päivitetään

  3. pip:llä käyttäjäkohtaisesti
    * - ei automaattisia päivityksiä
    * + hyvin eristetty, ei häiritse muuta järjestelmää
    * + pystyy jakamaan projektien kesken

  4. pip:llä projektikohtaisesti (virtualenv)
    * - vie turhaan tilaa
    * - vaatii (vähän) erillistä työtä aina otettaessa projektia käyttöön
    * + hyvin eristetty
    * + taatusti halutut versiot
    * + pystyy ajamaan eristettyjä buildeja esim. Dockerissa

