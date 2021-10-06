# spotify_app
A small Spotify app making use of the Spotify API and Rest Framework to display data

## Pre-requisite
The package `pipenv` is installed on machine

```
python -m pip install --user pipenv
```

Connect to a postgre database by informing the following environment variables:\
`POSTGRESQL_DATABASE_NAME`\
`POSTGRESQL_DATABASE_USER`\
`POSTGRESQL_DATABASE_PASSWORD`\
`POSTGRESQL_DATABASE_HOST`\
`POSTGRESQL_DATABASE_PORT`

Set the client ID and client secret from Spotify to allow authorization. This
can be obtained from [Spotify for developers](https://developer.spotify.com/)\
`CLIENT_ID`\
`CLIENT_SECRET`

These variables can be set in a `.env` file for local development.

## Install (locally)
This will install all necessary packages for local development.
```
pipenv install --dev
```

## Create and update database (Postgre)
```
pipenv run python manage.py migrate
```

## Listing all URLS of the server
Thanks to `django-extensions` package
```
pipenv run python manage.py show_urls
```

## Run server
The following command allows the server to run on localhost on port 5000.
This port is used for development so make sure to inform it.
```
pipenv run python manage.py runserver 5000
```

## Create super user
Creating a super user will permit fiddling with the django admin, which will,
in turn, allow you to manage the database.
```
pipenv run python manage.py createsuperuser
```

## Configure for production
Configure the following key should you require the application in production
```
BACKEND_SECRET_KEY=<crypto-strong key>
```

You can generate a crypto-strong key using the following command:
```
python -c "import secrets; print(secrets.token_hex(32))"
```
