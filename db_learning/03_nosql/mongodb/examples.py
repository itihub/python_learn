# 03_nosql/mongodb/examples.py

from crud import create_document, read_documents, update_document, delete_document
import datetime

# 创建文档
user_id = create_document('users', {'name': 'Bob', 'age': 25, 'created_at': datetime.now()})
print(f"创建用户，ID：{user_id}")

# 读取文档
users = read_documents('users')
print(f"所有用户：{users}")

# 更新文档
update_count = update_document('users', {'name': 'Bob'}, {'age': 26})
print(f"更新用户数：{update_count}")

# 删除文档
delete_count = delete_document('users', {'name': 'Bob'})
print(f"删除用户数：{delete_count}")