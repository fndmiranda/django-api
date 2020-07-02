# Django Api

A Django boilerplate for Api, with OAuth2 authentication, api documentation with Swagger,
account management with forgot password and retrieve by email.

# Requirements

* Python (3.8)

## Installation and configure

### Clone

Execute the following command to get the latest version of the project:

```terminal
$ git clone git@github.com:fndmiranda/django-api.git django-api
```

### Environment variables

Copy and change front variables according to your environment:

```terminal
$ cd django-api
$ cp .env.example .env
```

### Install dependencies

Execute the following command to install project dependencies:

```terminal
$ pip install -r requirements/development.txt
```

## Run

Execute the following command to execute updates database schema. Manages both apps with migrations and those without:

```terminal
$ make migrate
```

Execute the following command to create a superuser:

```terminal
$ make createsuperuser
```

Execute the following command to create a OAuth2 application on the Authorization server:

```terminal
$ make createoauthapplication
```

Execute the following command to execute development server:

```terminal
$ make runserver
```

Execute the following command to creates new migration(s) for apps:

```terminal
$ make makemigrations
```

Execute the following command to execute tests:

```terminal
$ make test
```

Execute the following command to execute flake8:

```terminal
$ make flake8
```

Execute the following command to list outdated packages:

```terminal
$ make outdated
```

# Translation

Execute the following command to runs over the entire source tree of the current directory and pulls 
out all strings marked for translation:

Change `pt_BR` to your locale

```terminal
$ make makemessages locale=pt_BR
```

Execute the following command to compiles .po files to .mo files for use with builtin gettext support:

Change `pt_BR` to your locale

```terminal
$ make compilemessages locale=pt_BR
```

# Links

After run `make runserver`

In your browser go to the `http://127.0.0.1:8000/admin/` address to access Django Admin

## Api documentation

* A JSON view of your API specification at `http://127.0.0.1:8000/swagger.json`
* A YAML view of your API specification at `http://127.0.0.1:8000/swagger.yaml`
* A swagger-ui view of your API specification at `http://127.0.0.1:8000/swagger/`
* A built-in view of your API specification at `http://127.0.0.1:8000/docs/`
* A JS built-in view of your API specification at `http://127.0.0.1:8000/docs/schema.js`
* A ReDoc view of your API specification at `http://127.0.0.1:8000/redoc/`