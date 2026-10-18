up:
	docker compose up --build -d

down:
	docker compose down -v

test-catalog:
	docker compose -f compose.test.yml up --build -d
	set -a; . ./.env; set +a; \
	PYTHONPATH=backend/catalog-service/src \
	CAT_DB_HOST=localhost CAT_DB_PORT=5434 CAT_DB_NAME=catalog_test \
	S3_ENDPOINT_URL=http://localhost:9002 S3_PUBLIC_URL=http://localhost:9002 \
	pytest backend/catalog-service/tests/