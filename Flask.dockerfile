FROM python:3.9
COPY LAN_forwarder.py LAN_forwarder.py
COPY my_celery_app.py my_celery_app.py
COPY tasks.py tasks.py
COPY requirements.txt requirements.txt
COPY secrets.json secrets.json
COPY utils.py utils.py
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "LAN_forwarder:app"]