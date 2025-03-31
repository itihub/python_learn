from sqlalchemy.orm import Session
from sqlalchemy import insert
from models import Actor, engine

session = Session(engine)


def create_user():
    squidward = User(name="squidward", fullname="Squidward Tentacles")
    # 调用该方法时，对象处于待处理状态，尚未插入
    session.add(squidward)
    # 查看状态
    print(session.new)
    # 向数据库发出 SQL 以退出当前的更改集时，该过程称为刷新
    # 手动将待处理的更改推送到当前事务，但通常没有必要，因为该 功能具有称为autoflush 的Session行为，
    session.flush()
    # 提交事物
    session.commit()