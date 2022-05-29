all: build

build:
	docker-compose build

run:
	docker-compose -f docker-compose.yml --env-file config/dev.env up

connect:
	docker-compose exec app bash

connect-db:
	docker-compose -–env-file config/dev.env exec postgres psql -h localhost -U movies movies

redo-db:
	docker-compose –-env-file config/dev.env rm -v postgres