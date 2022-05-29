all: build

build:
	docker-compose build

cli:
	docker-compose –env-file config/dev.env up

connect:
	docker-compose exec app bash

connect-db:
	docker-compose –env-file config/dev.env exec postgres psql -h localhost -U movies movies

redo-db:
	docker-compose –env-file config/dev.env rm -v postgres