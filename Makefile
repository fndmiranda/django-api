env-test:
    export DATABASE_ENGINE=django.db.backends.sqlite3

runserver:
	@python manage.py runserver --settings=core.settings

migrate:
	@python manage.py migrate --settings=core.settings

createsuperuser:
	@python manage.py createsuperuser --settings=core.settings

createoauthapplication:
	@python manage.py createoauthapplication --settings=core.settings

makemigrations:
	@python manage.py makemigrations --settings=core.settings

test: env-test
	@py.test -s

makemessages:
	@python manage.py makemessages -l $(locale)

compilemessages:
	@python manage.py compilemessages --locale=$(locale)

outdated:
	@pip list --outdated

flake8:
	@flake8 --show-source .
