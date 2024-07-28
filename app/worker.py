import asyncio

from arq import Retry
from arq.connections import RedisSettings


async def startup(ctx):
    print("Worker started")


async def shutdown(ctx):
    print("Worker shutting down")


async def create_task(ctx, sleep_time: int):
    # simulate long-running computation here
    print(f'{ctx}')
    print(f"Running job {ctx['job_id']} created at {ctx['enqueue_time'].isoformat()} try #{ctx['job_try']}")
    if sleep_time >= 4:  # simulate an exception
        print("Too long!")
        # retry the job with increasing back-off
        # delays will be 5s, 10s, 15s, 20s, 25s
        # after max_tries (default 5) the job will permanently fail
        raise Retry(defer=ctx['job_try'] * 5)
    await asyncio.sleep(sleep_time)
    print("Done!")


FUNCTIONS: list = [
    create_task,
]


class WorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings()
    functions: list = FUNCTIONS
