from celery import Celery
from config import CONFIG_GLOB

app = Celery('worker_preprocess', broker=CONFIG_GLOB.REDIS_URL)

@app.task(name="preprocessor")
def preprocess(data):
    # Process raw sound data
    sound_level = data['sound_level']  # e.g., dB
    frequency = data['frequency']        # e.g., Hz
    # Normalize and prepare data
    # Store in database (not shown here)

    return {"status": "processed"}
