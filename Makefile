up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	python answer.py

reset:
	make down && make up && make migrate

load:
	python load.py