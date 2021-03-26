![run-yamdb](https://github.com/volhadounar/foodgram-project/workflows/foodgram_workflow/badge.svg)

Site Foodgram
=================================
This is an online service where users can publish recipes, subscribe to another user, add recipes to the favorite list, and download a summary list of products needed to prepare one or more selected dishes before going to the store.

The project is deployed at a remote server http://saludformula.tk (http://178.154.198.136)
You can folow admin site http://saludformula.tk/admin/ or 
http://178.154.198.136/admin using credentials: username:admin, password:2203.

Tech stack: Python3, Django Framework, HTTP, HTTPS, Pillow, django-filter,  Gunicorn, Nginx, Linux, Docker, Visual Studio Code, Yandex Cloud, GitHubActions.

Getting Started
===============

1. You can build it in steps:
    1. ``cd ...wherever...``
    2. ``git clone https://github.com/volhadounar/foodgram-project.git``
    3. ``cd foodgram-project``
    4. ``touch .env`` -- creates .env file for postgresql, add keys: DB_NAME=postgres, POSTGRES_USER=postgres, POSTGRES_PASSWORD=postgres, DB_HOST=db, DB_PORT=5432
    4. ``docker-compose up`` -- the project will unfold in 3 containers using web image on DockerHub volhadounar87/foodgram:v1.2021, nginx:1.19-alpine, postgres:12.4 
    5. Open another command window.
    6. ``docker-compose run web python manage.py migrate`` -- Reads all the migrations folders in the application folders and creates / evolves the tables in the database
    7. ``docker-compose exec web python manage.py createsuperuser``
    8. ``docker-compose exec web python manage.py loaddata fixtures.json`` -- Uploads fixtures file with web-service' data

