import time
from celery import Celery

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task
def add(x, y):
    time.sleep(1)
    print(f"Adding {x} + {y}")
    return x + y
