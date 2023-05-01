from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI(title = "Tasks",prefix = "/tasks")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-18911.c277.us-east-1-3.ec2.cloud.redislabs.com",
    port=18911,
    password="ZybwlYc37F9kk33ysDB3SXhC853B1iIv",
    decode_responses=True
)


class Task(HashModel):
    title: str
    description: str
    completed: int
    is_valid_user: int

    class Meta:
        database = redis


@app.get('/')
def all():
    return [format(pk) for pk in Task.all_pks()]


def format(pk: str):
    task = Task.get(pk)

    return {
        'id': task.pk,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'is_valid_user':task.is_valid_user
    }


@app.post('/')
def create(task: Task):
    return task.save()


@app.get('/{pk}')
def get(pk: str):
    return Task.get(pk)


@app.delete('/{pk}')
def delete(pk: str):
    return Task.delete(pk)