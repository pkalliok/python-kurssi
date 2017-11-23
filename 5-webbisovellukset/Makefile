
.PHONY: all test
all: test

test: stamps/local-flask.pid
	(. myenv/bin/activate && nose2)

stamps/create-virtualenv:
	virtualenv -p python3 myenv
	(. myenv/bin/activate && pip install -r requirements.txt)
	touch $@

PIDFILE=stamps/local-flask.pid
$(PIDFILE): stamps/create-virtualenv
	(. myenv/bin/activate \
	&& FLASK_APP=webapp.py flask run -p 3000 > "$@.log" 2>&1 \
	& echo "$$!" > "$@")
	until curl http://localhost:3000/; do \
		sleep 1; echo -n "retrying..."; done
	@echo ... service up and running.

.PHONY: stop-local-flask
stop-local-flask:
	kill "`cat $(PIDFILE)`" && rm "$(PIDFILE)"

