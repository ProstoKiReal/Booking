TEST_BOOKING_COMPOSE = docker compose -p booking-tests -f backend/booking-service/compose.test.yml

.ONESHELL:
test-booking:
	@set +e
	$(TEST_BOOKING_COMPOSE) up --build -d booking-test-db booking-test-app
	start_status=$$?
	if [ $$start_status -ne 0 ]; then
		$(TEST_BOOKING_COMPOSE) down --volumes
		exit $$start_status
	fi
	$(TEST_BOOKING_COMPOSE) run --build --rm booking-test-runner
	test_status=$$?
	$(TEST_BOOKING_COMPOSE) down --volumes
	cleanup_status=$$?
	if [ $$test_status -ne 0 ]; then exit $$test_status; fi
	exit $$cleanup_status

up:
	docker compose up --build -d

down:
	docker compose down -v
