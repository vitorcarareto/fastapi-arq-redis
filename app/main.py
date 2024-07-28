import random

from arq.connections import ArqRedis, create_pool
from arq.connections import RedisSettings
from arq.jobs import Job
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


class TaskModel(BaseModel):
    count: int = Field(
        title="How many tasks to generate? (1 to 100)", ge=1, le=100)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('home.html', {
        'request': request,
        'min': 1,
        'max': 100,
    })


@app.get("/task/{job_id}")
async def get_task(job_id: str):
    queue: ArqRedis = await create_pool(RedisSettings())
    job = Job(job_id=job_id, redis=queue)
    status = await job.status()
    result = await job.result()
    return {
        'job_id': job_id,
        'status': status,
        'result': result,
    }


@app.post("/task", status_code=201)
async def task(task: TaskModel):
    queue: ArqRedis = await create_pool(RedisSettings())
    task_ids: list = []
    for i in range(task.count):
        sleep_time = random.randint(1, 5)
        job = await queue.enqueue_job('create_task', sleep_time)
        task_ids.append(job.job_id)
    return {
        "queued": task.count,
        "task_ids": task_ids,
    }
