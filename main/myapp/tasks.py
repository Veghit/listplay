import sys
sys.path.insert(0, '/home/LISTPLAY1/LISTPLAY/celery-3.1.11/celery-test/.python/bin/')
from celery import Celery

app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y