from main import redis, Task
import time

key = 'user_activated'
group = 'user-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                try:
                    task = Task.get(obj['task_id'])
                    task.is_valid_user = 1
                    product.save()
                except:
                    redis.xadd('error', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)