SOURCE=$(wildcard src/*.py)
TESTS=$(wildcard nosetests/*.py)

stamps/create-virtualenv:
	virtualenv -p python3 myenv
	(. myenv/bin/activate && pip install -r requirements.txt)
	touch $@

