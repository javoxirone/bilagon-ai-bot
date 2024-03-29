import os
from celery import Celery

app = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)


@app.task
def delete_handled_file(path: str) -> None:
    try:
        os.remove(path)
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")
