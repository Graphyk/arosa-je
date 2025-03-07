init: ##initialize the project
	@$(MAKE) stop
	@$(MAKE) start
	@$(MAKE) migrate

start: ## start back + front
	@docker compose up -d

stop: ## stop all containers
	@docker compose stop

make-migrations:  ## make migrations
	@docker compose exec  backend python3 manage.py makemigrations

migrate: ## apply migrations
	@docker compose exec  backend python3 manage.py migrate