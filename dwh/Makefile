.PHONY: build start stop delete

build:
	docker build --rm -t dwh-postgres-image .
	docker volume create --name dwh-postgres-volume

start:
	docker run --rm --name dwh-postgres --volume dwh-postgres-volume:/var/lib/postgresql/data -p 5432:5432 -d dwh-postgres-image

stop:
	docker stop dwh-postgres

delete:
	docker volume rm dwh-postgres-volume
