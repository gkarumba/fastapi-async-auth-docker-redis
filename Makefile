up:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

migrate:
	docker-compose exec api uv run alembic upgrade head

revision:
	docker-compose exec api uv run alembic revision --autogenerate -m "update"

shell:
	docker-compose exec api sh