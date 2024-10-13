## Combination.
- Celery + FastAPI + Flower + Docker

### 1. Celery
- To execute dockerized executing tools
### 2. FastAPI
- To provide user familiar interface throughout webpages
### 3. Flower
- To monitor each worker's process load status
### 4. Docker
- Executing each tools without dependency.


## Structure (Simple)
Users #0 -----+----- Fast API ----+----> Rabbit MQ ---------+------> Celery Worker #0
              |                   |                         |
Users #1 -----+----- Fast API ----┤                         |
              |                   |                         |
Users #2 -----+----- Fast API ----┤  +--- Redis MQ <--------┤
              |                   |  |                      |
Users #3 -----+----- Fast API ----+<-+                      +------> Celery Worker #1


![alt text](image.png)

### Reference Pages
- https://testdriven.io/courses/fastapi-celery/getting-started/

### Prerequisite
1. Docker install
on MacOs :: $ brew install docker --cask

1.1 Docker image download and run
$ 
$ docker run -p 6379:6379 --name <redis-name> -d redis
// Actual : docker run -p 6379:6379 --name hope-redis -d redis
$ docker exec -it <redis-name> redis-cli ping
// Actual : docker exec -it hope-redis redis-cli ping

1.2 poetry installation for python version management
* Globally installed and set the PATH
`$ curl -sSL https://install.python-poetry.org | python3 -`

>> /Users/hope/.local/bin is installed directory.

>> Trouble Shooting
```
File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/venv/__init__.py", line 31, in should_use_symlinks
    raise Exception("This build of python cannot create venvs without using symlinks")
Exception: This build of python cannot create venvs without using symlinks
```
Then, install pyenv
$ brew install pyenv --cask
or
$ brew install poetry // it works!

* Need to set PATH env for poetry, not needed when using brew

1.3 Poetry Usage
`$ poetry install` installs python package defined at `.toml` following dependencies.
`$ poetry shell` can activate virtual environment.
`$ poetry add` can add and install packages, for example `poetry add requests`
Refers details this site.
https://velog.io/@qlgks1/python-poetry-%EC%84%A4%EC%B9%98%EB%B6%80%ED%84%B0-project-initializing-%ED%99%9C%EC%9A%A9%ED%95%98%EA%B8%B0

1.3.1 How to run poetry?
$ poetry run main:app

1.3.2 What if there's problem on version management with poetry
$ poetry export --without-hashes -o requirements.txt
$ poetry add djangorestframework==3.13.1

#2. Celery Examples
##Celery task define
- @celery.task : Annotate specific function is celery's task
- function.delay(arg1, arg2, ...) : 
- Result saving
```python
task = divide.delay(1, 2)
type(task) # <class 'celery.result.AsyncResult'>
print(task.state, task.result)
```

>> poetry run celery -A main.celery worker --loglevel=info
>> poetry run celery -A main.celery flower --port=5555


#99. References
Celery Concurrency : https://postbarca.tistory.com/76





-------------------------------------------------------------------------------------

+------------------+       +------------------+       +------------------+
|                  |       |                  |       |                  |
|   FastAPI Server +<----->+    Celery Worker +<----->+    KPI_CAL       |
|                  |       |                  |       |   Docker Images   |
+------------------+       +------------------+       +------------------+
          ^                          |
          |                          |
          |                          |
+------------------+       +------------------+
|                  |       |                  |
|    Redis Queue   |       |  Database        |
|                  |       |                  |
+------------------+       +------------------+


<코드 파일 구조>
kpi_system/
├── docker/
│   ├── kpi_system/
│   │   ├── Dockerfile
│   │   └── app/
│   │       ├── main.py
│   │       ├── tasks.py
│   │       ├── models.py
│   │       ├── database.py
│   │       └── frontend/
│   │           └── index.html
│   └── docker-compose.yml
└── requirements.txt


### Docker file 예시
`kpi_system/Dockerfile`
```docker
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

`docker-compose.yml`
```
version: '3.8'
services:
  redis:
    image: "redis:alpine"
  
  kpi_system:
    build:
      context: ./kpi_system
    ports:
      - "8000:8000"
    depends_on:
      - redis
```

### FastAPI
`app/main.py`
```
from fastapi import FastAPI, BackgroundTasks, HTTPException
from tasks import run_kpi_calculation
import docker

app = FastAPI()
client = docker.from_env()
MAX_CONTAINERS = 5

@app.post("/run-kpi/")
async def run_kpi(background_tasks: BackgroundTasks, kpi_type: str):
    # 현재 실행 중인 KPI_CAL 컨테이너 수 확인
    running_containers = [c for c in client.containers.list() if "KPI_CAL" in c.name]
    
    if len(running_containers) >= MAX_CONTAINERS:
        raise HTTPException(status_code=400, detail="Max container limit reached.")

    background_tasks.add_task(run_kpi_calculation, kpi_type)
    return {"message": "KPI calculation started", "kpi_type": kpi_type}
```

### Celery Tasks
`app/tasks.py`
```
from celery import Celery
import docker
from kpi_cal import calculate_kpi

app = Celery('tasks', broker='redis://redis:6379/0')
client = docker.from_env()

@app.task(bind=True, max_retries=3)
def run_kpi_calculation(self, kpi_type):
    container_name = f"kpi_cal_{kpi_type}_{self.request.id}"

    try:
        # KPI_CAL 이미지를 기반으로 컨테이너 생성 및 실행
        container = client.containers.run(
            f"your_dockerhub_user/kpi_cal:{kpi_type}",
            name=container_name,
            detach=True,
            auto_remove=True,
            environment={"KPI_TYPE": kpi_type}  # 필요시 환경변수 설정
        )
        
        # 컨테이너 로그 읽기 (KPI 계산 결과 얻기)
        logs = container.logs().decode("utf-8")
        # Save result to database (implement saving logic)
        
    except Exception as exc:
        raise self.retry(exc=exc)
```

### KPI 계산 로직
`app/kpi_cal.py`
```
def calculate_kpi(kpi_type):
    # KPI 계산 로직 구현
    if kpi_type == 'type1':
        # 계산 로직
        return "Result for KPI Type 1"
    elif kpi_type == 'type2':
        # 계산 로직
        return "Result for KPI Type 2"
    else:
        raise ValueError("Unknown KPI type")
```

### requirements.txt
```
fastapi
uvicorn
celery
redis
docker
sqlalchemy
```

### frontend
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KPI System</title>
</head>
<body>
    <h1>KPI Calculator</h1>
    <form action="/run-kpi/" method="post">
        <label for="kpi_type">KPI Type:</label>
        <input type="text" id="kpi_type" name="kpi_type" required>
        <button type="submit">Run KPI</button>
    </form>
</body>
</html>
```




1. Required Items for Implementation
Hardware:
Microcontroller (e.g., ESP32): Suitable for processing audio signals and connecting to Wi-Fi.
Price: Around $5-10.
Sound Sensor Module (e.g., MAX4466 or LM393): These sensors can detect sound levels and provide an analog or digital output.
Price: ~$5-10.
Microphone (if needed): If you want to capture sound more accurately, you can use a microphone with an appropriate amplifier.
Price: ~$5-15 (depending on the quality).
Breadboard and Jumper Wires: For connecting components.
Price: ~$5.
2. Two Different Celery Worker Processes
Worker 1: Preprocessing Raw Sound Data

Functionality: This worker receives raw sound data (e.g., sound level in dB and frequency) from the sound sensor, normalizes it, and prepares it for analysis.
Tasks:
Convert analog signals to digital (if necessary).
Extract volume (in dB) and frequency data (in Hz).
Store preprocessed data in the database.
Worker 2: Analyzing Sound Quality

Functionality: This worker retrieves preprocessed sound data and analyzes it to determine if the sound quality is within acceptable limits.
Tasks:
Check if the volume levels are within a desirable range (e.g., 60-80 dB).
Analyze frequency ranges to determine if they are uncomfortable (e.g., frequencies above 20 kHz or below 20 Hz).
Trigger alerts if sound levels or frequencies are outside acceptable ranges.



/iot_sound_monitor
|-- /app
|   |-- __init__.py               # Initialize the app
|   |-- main.py                   # FastAPI application
|   |-- static/                    # Static files (CSS, JS)
|   |   |-- style.css              # CSS styles
|   |   |-- script.js              # JavaScript for frontend
|   |-- templates/                 # HTML templates
|   |   |-- index.html             # Main HTML page
|   |-- worker_preprocess.py       # Worker for preprocessing
|   |-- worker_analyze.py          # Worker for analysis
|-- Dockerfile                      # Dockerfile for building the app
|-- docker-compose.yml              # Docker Compose configuration
|-- requirements.txt                # Python dependencies


redis:127.0.0.1:6379/0




'Poetry Add 필요한 것들'
$ poetry add jinja2
$ poetry add python-multipart