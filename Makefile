.PHONY: help build up down restart restart-all logs shell migrate makemigrations-check createsuperuser collectstatic test lint setwebhook deletewebhook webhookinfo

help:
	@echo "Available targets:"
	@echo "  build          - docker compose build"
	@echo "  up             - docker compose up -d"
	@echo "  down           - docker compose down"
	@echo "  restart        - restart django container"
	@echo "  restart-all    - restart django, celery, celery-beat, flower"
	@echo "  logs           - follow logs"
	@echo "  shell          - open django shell"
	@echo "  migrate        - run migrations"
	@echo "  createsuperuser- create admin user"
	@echo "  collectstatic  - collect static files"
	@echo "  test           - run Django tests"
	@echo "  lint           - basic flake8 lint (if installed)"
	@echo "  setwebhook     - set Telegram webhook"
	@echo "  deletewebhook  - delete Telegram webhook"
	@echo "  webhookinfo    - get current webhook info"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart django

restart-all:
	docker compose restart django celery celery-beat flower

logs:
	docker compose logs -f --tail=200

shell:
	docker compose exec django python manage.py shell

migrate:
	docker compose exec django python manage.py migrate

makemigrations-check:
	docker compose exec django python manage.py makemigrations --check --dry-run

createsuperuser:
	docker compose exec django python manage.py createsuperuser

collectstatic:
	docker compose exec django python manage.py collectstatic --noinput

test:
	docker compose exec django python manage.py test -v 2

lint:
	docker compose exec django flake8

setwebhook:
	docker compose exec django python manage.py setwebhook --drop-pending

deletewebhook:
	docker compose exec django python manage.py deletewebhook

webhookinfo:
	docker compose exec django python manage.py webhookinfo
