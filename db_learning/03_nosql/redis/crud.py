# 03_nosql/redis/crud.py

import redis
from common.config import REDIS_CONFIG

r = redis.Redis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'], db=REDIS_CONFIG['db'])

def set_value(key, value):
    r.set(key, value)

def get_value(key):
    return r.get(key)

def delete_value(key):
    r.delete(key)

# 示例用法
# set_value('name', 'Charlie')
# print(get_value('name'))
# delete_value('name')