SOURCE=$(wildcard src/*.py)
TESTS=$(wildcard nosetests/*.py)

.PHONY: all
all: stamps/run-tests

stamps/run-tests: $(PIDFILE) $(NOSETESTS)
	(. myenv/bin/activate && nose2)
	touch $@

stamps/create-virtualenv:
	virtualenv -p python3 myenv
	(. myenv/bin/activate && pip install -r requirements.txt)
	touch $@

PIDFILE=stamps/local-flask.pid
$(PIDFILE): stamps/create-virtualenv
	(. myenv/bin/activate \
	&& FLASK_APP=src/webapp.py FLASK_DEBUG=1 \
		flask run -p 3000 > "$@.log" 2>&1 \
	& echo "$$!" > "$@")
	until curl http://localhost:3000/ping; do \
		sleep 1; echo -n "retrying..."; done
	@echo ... service up and running.

.PHONY: stop-local-flask
stop-local-flask:
	kill "`cat $(PIDFILE)`" && rm "$(PIDFILE)"

.PHONY: run-local-gunicorn
run-local-gunicorn:
	gunicorn -b localhost:4000 src.webapp:app 

stamps/build-dependencies-image: requirements.txt docker/webapp-dependencies.docker
	cp requirements.txt docker/
	docker build -t webapp-dependencies \
		-f docker/webapp-dependencies.docker docker/
	touch $@

stamps/build-webapp-image: $(SOURCE) docker/webapp-application.docker
	cp -r src/ docker/
	docker build -t webapp-application \
		-f docker/webapp-application.docker docker/
	touch $@

