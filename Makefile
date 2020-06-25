env-test:
    export DATABASE_ENGINE=django.db.backends.sqlite3

runserver-dev:
	@python manage.py runserver --settings=core.settings

test: env-test
	py.test -s

outdated:
	@pip list --outdated

flake8:
	@flake8 --show-source .
