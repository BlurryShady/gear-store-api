# Gear Store API

Backend API for the Gear Store project.

A production-style Django REST Framework backend designed to be deployed on services like Render and consumed by a separate frontend (React + Vite).



## Tech stack

- Django
- Django REST Framework
- PostgreSQL (production)
- SQLite (local development)
- WhiteNoise (static files)



## Project structure

- `backend/`: Django project configuration (settings, urls, wsgi)
- `store/`: Core Django app (models, serializers, views, urls)
- `scripts/`: Backend utility/debug scripts
- `manage.py`: Django management entry point



## Local development

```powershell
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```

API will be available at:

http://127.0.0.1:8000/api/



## Environment variables

Create a .env file based on .env.example.

Important variables:

DJANGO_SECRET_KEY – secret key (required in production)

DATABASE_URL – e.g. postgres://USER:PASSWORD@HOST:PORT/DB

DJANGO_ALLOWED_HOSTS – comma-separated allowed hosts

DJANGO_CSRF_TRUSTED_ORIGINS – trusted frontend origins

DJANGO_CORS_ALLOWED_ORIGINS – allowed frontend origins

DEBUG – set to 0 in production



## Deploying on Render

Create a Render Web Service pointing to this repository.

Build command:

pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput


Start command:

gunicorn backend.wsgi


Set environment variables in Render dashboard (do not upload .env).

Attach a managed PostgreSQL database and set DATABASE_URL.

Add custom domain (e.g. api.store.blurryshady.dev) and update DJANGO_ALLOWED_HOSTS.



## Static & media files


Static files are served using WhiteNoise (STATIC_ROOT=staticfiles).

Media defaults to BASE_DIR/media.

For production, consider S3-compatible storage (recommended for Render).



## Testing / lint

```
py manage.py test
```




## License

MIT


[I've created this project to showcase in my website as portfolio project. You can check it out on store.blurryshady.dev](https://store.blurryshady.dev)