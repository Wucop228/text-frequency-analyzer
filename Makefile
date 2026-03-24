.PHONY: up down build logs restart migrate clean

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

logs:
	docker compose logs -f

logs-app:
	docker compose logs -f app

logs-db:
	docker compose logs -f db

restart:
	docker compose restart app

migrate:
	docker compose exec app alembic upgrade head

clean:
	docker compose down -v