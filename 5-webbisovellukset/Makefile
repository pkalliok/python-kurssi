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
	until curl -s http://localhost:3000/ping; do \
		sleep 1; echo -n "retrying..."; done
	@echo ... service up and running.

.PHONY: stop-local-flask
stop-local-flask:
	test -f "$(PIDFILE)" && kill "`cat $(PIDFILE)`" && rm "$(PIDFILE)"

.PHONY: run-local-gunicorn
run-local-gunicorn:
	gunicorn -b localhost:4000 src.webapp:app 

stamps/build-dependencies-image: requirements.txt docker/webapp-dependencies.docker
	cp requirements.txt docker/
	docker build -t webapp-dependencies \
		-f docker/webapp-dependencies.docker docker/
	touch $@

stamps/build-webapp-image: $(SOURCE) docker/webapp-application.docker stamps/build-dependencies-image
	cp -r src/ docker/
	docker build -t webapp-application \
		-f docker/webapp-application.docker docker/
	touch $@

stamps/run-image: stamps/build-webapp-image
	docker run -d -p 4000:4000 --name webapp-1 webapp-application
	until curl -s http://localhost:4000/ping; do \
		sleep 1; echo -n "retrying..."; done
	@echo ... service up and running.
	touch $@

.PHONY: stop-image
stop-image:
	docker rm -f webapp-1
	rm stamps/run-image

stamps/test-image: stamps/run-image
	(. myenv/bin/activate && SERVICE_ROOT=http://localhost:4000 nose2)
	touch $@

stamps/make-docker-login:
	docker login -u pkalliok
	touch $@

stamps/push-image: stamps/test-image stamps/make-docker-login
	docker tag webapp-application pkalliok/example-flask-webapp:latest
	docker push pkalliok/example-flask-webapp:latest
	touch $@

