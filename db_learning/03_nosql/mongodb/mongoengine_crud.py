# 03_nosql/mongodb/mongoengine_crud.py

from mongoengine_models import User

def create_user(name, age, email):
    user = User(name=name, age=age, email=email)
    user.save()
    return user.id

def read_users():
    return User.objects()

def read_user(user_id):
    return User.objects.filter(id=user_id).first()

def update_user(user_id, name=None, age=None, email=None):
    user = User.objects(id=user_id).first()
    if user:
        if name:
            user.name = name
        if age:
            user.age = age
        if email:
            user.email = email
        user.save()
        return user.id
    return None

def update_users():
    result = User.objects.filter(sex='male').update(inc__age=10)
    # 修改一条数据
    # result = User.objects.filter(sex='male').update_one(inc__age=100)
    return result


def delete_user(user_id):
    user = User.objects(id=user_id).first()
    if user:
        user.delete()
        return True
    return False

# 示例用法
# user_id = create_user('Alice', 30, 'alice@example.com')
# print(read_users())
# update_user(user_id, age=31)
# delete_user(user_id)