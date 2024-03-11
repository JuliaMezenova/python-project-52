install:
	poetry install

start_debug:
	poetry run python manage.py runserver

start:
	gunicorn task_manager.wsgi:application

test:
	poetry run python manage.py test

lint:
	poetry run flake8 task_manager

build:
	./build.sh

psql:
	sudo service postgresql start

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml
	poetry run coverage report
