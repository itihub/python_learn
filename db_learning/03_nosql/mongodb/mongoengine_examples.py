# 03_nosql/mongodb/mongoengine_examples.py

from mongoengine_crud import create_user, read_users, update_user, delete_user

# 创建用户
user_id = create_user('Bob', 25, 'bob@example.com')
print(f"创建用户，ID：{user_id}")

# 读取用户
users = read_users()
print(f"所有用户：{users}")

# 更新用户
update_id = update_user(user_id, age=26)
print(f"更新用户，ID：{update_id}")

# 删除用户
delete_result = delete_user(user_id)
print(f"删除用户结果：{delete_result}")