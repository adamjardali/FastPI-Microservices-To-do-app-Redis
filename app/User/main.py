from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time
from datetime import datetime

app = FastAPI(title = "Users")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# This should be a different database 
redis = get_redis_connection(
    host="redis-18911.c277.us-east-1-3.ec2.cloud.redislabs.com",
    port=18911,
    password="ZybwlYc37F9kk33ysDB3SXhC853B1iIv",
    decode_responses=True
)


class User(HashModel):
    task_id: str
    name: str
    password: str
    date_of_birth: datetime
    status: str  # completed, not-completed

    class Meta:
        database = redis


@app.get('/{pk}')
def get(pk: str):
    return User.get(pk)


@app.post('/')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()

    req = requests.get('http://localhost:8000/%s' % body['id'])
    task = req.json()
    user = User(
        task_id=body['id'],
        name=task['name'],
        password=task['password'],
        date_of_birth=task['date_of_birth'],
        status='pending'
    )
    user.save()

    # background_tasks.add_task(activate_user, user)

    return user


def activate_user(user: User):
    time.sleep(2)
    user.status = 'completed'
    user.save()
    redis.xadd('user_activated', user.dict(), '*')

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8001)