from main import redis, Order
import time

key = 'user_complete'
group = 'user-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            print(results)
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                user.status = 'complete'
                order.save()

    except Exception as e:
        print(str(e))
    time.sleep(1)