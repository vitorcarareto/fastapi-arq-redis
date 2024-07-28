import asyncio
import random

from arq.connections import ArqRedis, create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class TaskModel(BaseModel):
    count: int = Field(
        title="How many tasks to generate? (1 to 100)", ge=1, le=100)


async def create_task(ctx, sleep_time: int):
    # long-running computation here
    await asyncio.sleep(sleep_time)


@app.get("/")
async def index():
    return {"message": "Hello, world!"}


@app.post("/task", status_code=201)
async def task(task: TaskModel):
    queue: ArqRedis = await create_pool(RedisSettings())
    for i in range(task.count):
        sleep_time = random.randint(1, 10)
        await queue.enqueue_job('create_task', sleep_time)
    return {"queued": task.count}
