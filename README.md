# todo_app
Django ToDo application

Web Framework: Django

REST API Framework: Django REST Framework

JWT Library: Django REST Framework JWT

Swagger/OpenAPI documentation: drf-yasg

Database: PostgresSQL

WSGI server: Gunicorn

HTTP server for static content: Nginx

Deployment tools:
Git
Docker (Docker base image: python:3.8-slim-buster, this image is very stable and relatively small)

All project's dependencies and deployment chains are in files:
requirements.txt
Dockerfile
docker-compose.yml

Instructions how to launch the API:
1) Upload folder with files todo_app_production to a production server.
2) Correct IP address for production server in ALLOWED_HOSTS in todo_app_production\app\todo\settings.py
3) Build Docker container from folder todo_app_production at the production server (change password to real):
DB_PASS=password POSTGRES_PASSWORD=password docker-compose up --build
4) Create Django's createsuperuser:
DB_PASS=password POSTGRES_PASSWORD=password docker-compose run app sh -c "python manage.py createsuperuser"
5) Now it launched.
