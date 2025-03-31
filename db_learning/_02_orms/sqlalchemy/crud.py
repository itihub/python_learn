# 02_orms/sqlalchemy/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import insert
from models import Actor, engine

session = Session()


def insert():
    stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
    


def add():
    # 新增记录
    new_actor = Actor(first_name='PENELOPE', last_name='GUINESS')
    session.add(new_actor)
    session.commit()
    print("ID:", new_actor.id)

def add_all():
    # 批量新增记录
    session.add_all(
        Actor(first_name='NICK', last_name='WAHLBERG'),
        Actor(first_name='ED', last_name='CHASE'),
        Actor(first_name='JENNIFER', last_name='DAVIS'),
    )
    session.commit()

def get_one():
    # 查询数据
    actor = session.query(Actor).get(1)
    if actor:
        print("查询结果:", (actor.id, actor.first_name, actor.last_name, actor.last_update))
    else:
        print("没有此数据")

def query():
    # 查询数据
    actors = session.query(Actor).all()
    print("rows:", actors.count())
    print("查询结果:", [(actor.first_name, actor.last_name) for actor in actors])

def update():
    # 更新记录
    actor_to_update = session.query(Actor).filter(Actor.name == 'PENELOPE').first()
    if actor_to_update:
        actor_to_update.last_update = 33
        session.commit()

def delete(): 
    # 删除记录
    actor_to_delete = session.query(Actor).filter(Actor.first_name == 'Frank').first()
    if actor_to_delete:
        session.delete(actor_to_delete)
        session.commit()

session.close()