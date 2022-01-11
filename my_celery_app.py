
from celery import Celery

app = Celery(
    'my_celery',
    broker='amqp://localhost',
    include=['tasks']
)
