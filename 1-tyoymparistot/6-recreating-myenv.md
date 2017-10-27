myenv-hakemistossa ei ole mitään kovin arvokasta.  Tehdään säännöt,
joilla sen pystyy luomaan uudestaan:

```
[atehwa@undantag ~/proj/esim-python]$ vi Makefile 
[atehwa@undantag ~/proj/esim-python]$ cat Makefile 

all: myenv

myenv:
	virtualenv -p python3 myenv
	(. myenv/bin/activate && pip install -r requirements.txt)
```

Nyt sen pystyy luomaan uudelleen aina tarvittaessa:

```
(myenv) [atehwa@undantag ~/proj/esim-python]$ deactivate 
[atehwa@undantag ~/proj/esim-python]$ make
make: Nothing to be done for 'all'.
[atehwa@undantag ~/proj/esim-python]$ rm -r myenv/
[atehwa@undantag ~/proj/esim-python]$ make
virtualenv -p python3 myenv
Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /home/atehwa/proj/esim-python/myenv/bin/python3
Also creating executable in
/home/atehwa/proj/esim-python/myenv/bin/python
Installing setuptools, pip, wheel...done.
(. myenv/bin/activate && pip install -r requirements.txt)
Collecting nose2==0.6.5 (from -r requirements.txt (line 1))
Collecting nosy==1.2 (from -r requirements.txt (line 2))
Collecting six==1.11.0 (from -r requirements.txt (line 3))
  Using cached six-1.11.0-py2.py3-none-any.whl
Installing collected packages: six, nose2, nosy
Successfully installed nose2-0.6.5 nosy-1.2 six-1.11.0
[atehwa@undantag ~/proj/esim-python]$ . myenv/bin/activate
```

Lopuksi tietysti commit:

```
(myenv) [atehwa@undantag ~/proj/esim-python]$ git add Makefile 
(myenv) [atehwa@undantag ~/proj/esim-python]$ git commit -m "Rules for
recreating myenv"
[master c0bbf92] Rules for recreating myenv
 1 file changed, 7 insertions(+)
 create mode 100644 Makefile
```

