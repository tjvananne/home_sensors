FROM python:3.9
COPY tasks.py tasks.py
COPY my_celery_app.py my_celery_app.py
COPY requirements.txt requirements.txt
COPY secrets.json secrets.json
RUN pip install -r requirements.txt
CMD ["celery", "-A", "my_celery_app", "worker", "--pool=eventlet", "--loglevel=INFO"]