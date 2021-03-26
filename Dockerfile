FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY /recipe_community .
RUN python manage.py collectstatic --noinput
CMD gunicorn recipe_community.wsgi:application --bind 0.0.0.0:8000
