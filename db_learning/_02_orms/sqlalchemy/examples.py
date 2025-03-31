# 02_orms/sqlalchemy/examples.py

from sqlalchemy.orm import Session
from models import User
from crud import session, users

print("所有用户：", users)

new_user = User(name="Grace", age=27)
session.add(new_user)
session.commit()

print("添加用户后：", session.query(User).all())

session.close()
