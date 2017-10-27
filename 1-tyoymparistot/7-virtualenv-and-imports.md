Virtualenv ei oikeasti tee mitään kovin maagista.  Se lisää Pythonin
kirjastopolkuun muutaman oman hakemistonsa, ja $PATH:iin hakemiston
jossa on tietyt versiot binääreistä.

```
(myenv) [atehwa@undantag ~/proj/esim-python]$ deactivate
[atehwa@undantag ~/proj/esim-python]$ echo $PATH
/home/atehwa/bin:/home/atehwa/bin:/home/atehwa/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/atehwa/Android/Sdk/tools:/home/atehwa/Android/Sdk/platform-tools
[atehwa@undantag ~/proj/esim-python]$ python3 -c 'import sys; print(sys.path)'
['', '/usr/lib/python35.zip', '/usr/lib/python3.5',
'/usr/lib/python3.5/plat-x86_64-linux-gnu',
'/usr/lib/python3.5/lib-dynload',
'/home/atehwa/.local/lib/python3.5/site-packages',
'/usr/local/lib/python3.5/dist-packages',
'/usr/lib/python3/dist-packages']
[atehwa@undantag ~/proj/esim-python]$ . myenv/bin/activate
(myenv) [atehwa@undantag ~/proj/esim-python]$ echo $PATH
/home/atehwa/proj/esim-python/myenv/bin:/home/atehwa/bin:/home/atehwa/bin:/home/atehwa/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/atehwa/Android/Sdk/tools:/home/atehwa/Android/Sdk/platform-tools
(myenv) [atehwa@undantag ~/proj/esim-python]$ python3 -c 'import sys; print(sys.path)'
['', '/home/atehwa/proj/esim-python/myenv/lib/python35.zip',
'/home/atehwa/proj/esim-python/myenv/lib/python3.5',
'/home/atehwa/proj/esim-python/myenv/lib/python3.5/plat-x86_64-linux-gnu',
'/home/atehwa/proj/esim-python/myenv/lib/python3.5/lib-dynload',
'/usr/lib/python3.5', '/usr/lib/python3.5/plat-x86_64-linux-gnu',
'/home/atehwa/proj/esim-python/myenv/lib/python3.5/site-packages']
```

Pythonin import ei myöskään tee mitään kovin maagista.  Se etsii
skriptin, suorittaa sen, ja jos skripti luo joitain nimiä, niistä tulee
importilla luodun module-olion jäseniä:

```
(myenv) [atehwa@undantag ~/proj/esim-python]$ vi kokeilu.py
(myenv) [atehwa@undantag ~/proj/esim-python]$ cat kokeilu.py 

print("Moi, oon mukamas moduuli")
aarre = 3
def jotain(): print("Hilloo!")

(myenv) [atehwa@undantag ~/proj/esim-python]$ python3
Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import kokeilu
Moi, oon mukamas moduuli
>>> kokeilu.aarre
3
>>> kokeilu.jotain
<function jotain at 0x7fb3e2636950>
>>> kokeilu.jotain()
Hilloo!
```

Pythonissa kaikki nimet (scopessa olevat tai jäsenten nimet) ovat
käytännössä vain viittauksia/osoittimia johonkin.

```
>>> f = kokeilu.jotain
>>> f()
Hilloo!
>>> kokeilu2 = kokeilu
>>> kokeilu2.aarre
3
>>> kokeilu2.aarre = 5
>>> kokeilu.aarre
5
```

