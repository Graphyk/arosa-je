init: ##initialize the project
	rm -r backend/db.sqlite3
	@$(MAKE) stop
	@$(MAKE) start
	@$(MAKE) migrate
	@docker compose exec  backend python3 manage.py createsuperuser --noinput --email admin@arosaje.com --username admin
	@docker compose exec  backend python3 manage.py shell -c "from django.contrib.auth import get_user_model;User = get_user_model();user = User.objects.get(username='admin');user.set_password('admin');user.save()"

start: ## start back + front
	@docker compose up -d

stop: ## stop all containers
	@docker compose stop

make-migrations:  ## make migrations
	@docker compose exec  backend python3 manage.py makemigrations

migrate: ## apply migrations
	@docker compose exec  backend python3 manage.py migrate