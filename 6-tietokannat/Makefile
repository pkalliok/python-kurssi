SOURCE=$(wildcard src/*.py) $(wildcard src/sql/*.sql)
TESTS=$(wildcard nosetests/*.py)

stamps/create-virtualenv:
	virtualenv -p python3 myenv
	(. myenv/bin/activate && pip install -r requirements.txt)
	touch $@

stamps/start-database:
	docker run -d -p 15432:5432 --name python-postgres-1 \
		-e POSTGRES_PASSWORD=veryhard postgres
	until nc -z localhost 15432; do echo -n .; sleep 1; done
	@echo database is up.
	touch $@

stamps/create-database: stamps/start-database
	docker run -it --rm --link python-postgres-1:postgres \
		-v "`pwd`/scripts/initdb.sql":/var/tmp/initdb.sql \
		-e PGPASSWORD=veryhard postgres \
		psql -h postgres -U postgres --no-password \
			-f /var/tmp/initdb.sql
	touch $@

.PHONY: stop-database
stop-database:
	docker rm -f python-postgres-1
	rm stamps/start-database

stamps/run-tests: stamps/create-database $(SOURCE) $(TESTS)
	(. myenv/bin/activate && nose2)
	touch $@

