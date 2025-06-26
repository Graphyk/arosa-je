help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: ##initialize the project
	@$(MAKE) stop
	@docker compose up -d
	@$(MAKE) migrate
	@$(MAKE) load-fixtures

start: ## start back + front
	@docker compose up -d

stop: ## stop all containers
	@docker compose stop

make-migrations:  ## make migrations
	@docker compose exec  backend python3 manage.py makemigrations

migrate: ## apply migrations
	@docker compose exec  backend python3 manage.py migrate

load-fixtures: 
	@docker compose exec  backend python3 manage.py loaddata address species plants posts user keeping consentment

test:
	@docker compose exec  backend python3 manage.py test arosaje.tests

django-shell:
	@docker compose exec  backend python3 manage.py shell