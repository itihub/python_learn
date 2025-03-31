# 02_orms/peewee/crud.py

from models import User

# 创建用户
User.create(name='Henry', age=34)

# 查询用户
users = User.select()
print("查询结果:", [(user.name, user.age) for user in users])

# 更新用户
user_to_update = User.get(User.name == 'Henry')
user_to_update.age = 36
user_to_update.save()

# 删除用户
user_to_delete = User.get(User.name == 'Henry')
user_to_delete.delete_instance()