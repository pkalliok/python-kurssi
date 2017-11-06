
all: myenv stamps/install-stopwords

myenv:
	virtualenv -p python3 myenv
	(. myenv/bin/activate && pip install -r requirements.txt)

stamps/install-stopwords:
	(. myenv/bin/activate && python -c 'import nltk; nltk.download("stopwords")')
	touch $@

