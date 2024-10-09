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
