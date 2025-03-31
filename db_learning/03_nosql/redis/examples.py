# 03_nosql/redis/examples.py

from crud import set_value, get_value, delete_value

# 设置键值对
set_value('age', 35)
print(f"获取年龄：{get_value('age')}")

# 删除键值对
delete_value('age')
print(f"删除年龄后：{get_value('age')}")