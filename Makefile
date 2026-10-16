TEST_CATALOG_COMPOSE = docker compose -p catalog-tests -f backend/catalog-service/compose.test.yml

.ONESHELL:
test-catalog:
	@set +e
	$(TEST_CATALOG_COMPOSE) up --build -d catalog-test-db catalog-test-app
	start_status=$$?
	if [ $$start_status -ne 0 ]; then
		$(TEST_CATALOG_COMPOSE) down --volumes
		exit $$start_status
	fi
	$(TEST_CATALOG_COMPOSE) run --build --rm catalog-test-runner
	test_status=$$?
	$(TEST_CATALOG_COMPOSE) down --volumes
	cleanup_status=$$?
	if [ $$test_status -ne 0 ]; then exit $$test_status; fi
	exit $$cleanup_status

up:
	docker compose up --build -d

down:
	docker compose down -v
