install:
	poetry install

start_debug:
	poetry run python manage.py runserver

start:
	gunicorn task_manager.wsgi:application

test:
	poetry run coverage run --source='.' manage.py test

lint:
	poetry run flake8 task_manager

build:
	./build.sh