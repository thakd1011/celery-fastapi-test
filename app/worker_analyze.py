from celery import Celery
from config import CONFIG_GLOB

app = Celery('worker_analyze', broker=CONFIG_GLOB.REDIS_URL)

@app.task(name="analyzer")
def analyze(data):
    sound_level = data['sound_level']
    frequency = data['frequency']
    
    # Check sound level
    if sound_level < 60 or sound_level > 80:
        return {"alert": "Sound level out of range!"}
    
    # Check frequency range
    if frequency < 20 or frequency > 20000:
        return {"alert": "Frequency out of range!"}
    
    return {"status": "sound quality is good"}
