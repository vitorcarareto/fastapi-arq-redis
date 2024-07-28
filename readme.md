This project demonstrates a setup using FastAPI, Redis, and ARQ for efficient background task processing.

## Architecture Overview

The system consists of three main components:

1. [FastAPI](https://fastapi.tiangolo.com/) Application:

- A web framework that handles incoming API requests.
- Enqueues background tasks to Redis when specific API endpoints are called.

2. [Redis](https://hub.docker.com/_/redis):

- An in-memory data structure store, used here as a message broker.
- Manages the task queue and ensures reliable task delivery between the FastAPI application and the ARQ worker.

3. [ARQ](https://github.com/python-arq/arq) Worker:

- A background worker that fetches tasks from the Redis queue.
- Processes the enqueued tasks asynchronously.

## Setup

- Setup a python virtual environment and install the required dependencies.

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the application

- Run Redis, FastAPI app and ARQ worker

```shell
./run_redis.sh
./run_app.sh
./run_worker.sh
```

## Handling tasks (pub/sub)

### Enqueueing Tasks

- You can enqueue tasks by calling the API endpoint that creates and enqueues background tasks:
  http://127.0.0.1:8000/docs#/default/task_task_post

### Processing Tasks

- Once tasks are enqueued, the ARQ worker will automatically pick them up from the Redis queue and process them
  asynchronously. The worker handles task execution, retries, and error management, ensuring robust and efficient
  background processing.
