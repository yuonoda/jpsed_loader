up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	python migrate.py

reset:
	make down && make up

load:
	python load.py