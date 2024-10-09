from fastapi import FastAPI
from celery import Celery

app = FastAPI()

celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0", # Can define these broker, backend value into seperate config file or pull them from environment file.
    backend="redis://127.0.0.1:6379/0"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@celery.task # Send a task to celery worker
def divide(x, y):
    """divide x by y after sleeping 5 seconds"""
    import time
    time.sleep(5)
    return x / y