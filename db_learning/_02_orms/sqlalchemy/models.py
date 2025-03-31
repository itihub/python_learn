# 02_orms/sqlalchemy/models.py
"""

"""

from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, text, select, func
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship, Session)
from sqlalchemy.orm import sessionmaker
from db_learning.common.config import MYSQL_CONFIG

#  建立连接-数据库引擎
DATABASE_URL = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}?charset={MYSQL_CONFIG['charset']}"
engine = create_engine(
    DATABASE_URL,
    echo=True,  # echo 设为 True 会打印出实际执行的 sql，调试的时候更方便
    future=True,  # 使用 SQLAlchemy 2.0 API，向后兼容
    pool_size=5, # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
    pool_recycle=3600, # 设置时间以限制数据库自动断开  
)

# 配置会话工厂：sessionmaker 是一个会话工厂，用于创建与数据库交互的 Session 对象
# bind=engine：将会话与之前创建的 engine 绑定，确保会话可以通过引擎连接到数据库。
# Session 对象：是与数据库交互的核心对象，负责执行查询、插入、更新和删除操作。
Session = sessionmaker(bind=engine)

# 声明基础模型类，declarative_base 是 SQLAlchemy 提供的一个函数，用于创建一个基础类，所有 ORM 模型类都需要继承它。
class Base(DeclarativeBase):
    pass

# 声明模型类
class User(Base):
    #  表名
     __tablename__ = "user_account"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(30))
     fullname: Mapped[Optional[str]] = mapped_column(String(30))

     addresses: Mapped[List["Address"]] = relationship(back_populates="user")

     def __repr__(self) -> str:
         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
     
class Address(Base):
     __tablename__ = "address"

     id: Mapped[int] = mapped_column(primary_key=True)
     email_address: Mapped[str] = mapped_column(String(255), nullable=False)
     # 外键
     user_id = mapped_column(ForeignKey("user_account.id"))

     user: Mapped[User] = relationship(back_populates="addresses")

     def __repr__(self) -> str:
         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
     

# 旧版声明式映射使用Column对象以及使用declarative_base()函数创建基类
class Actor(Base):
    __tablename__ = 'actor'
    id = Column('actor_id', Integer, primary_key=True)
    first_name = Column(String(45))
    last_name = Column(String(45))
    last_update = Column(DateTime)

# 从 ORM 映射发送 DDL 到数据库
Base.metadata.create_all(engine)


def insert():
    """
    类的实例代表行
    """
    squidward = User(name="squidward", fullname="Squidward Tentacles")
    krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

    print(squidward)

    with Session(engine) as session:
        session.add(squidward)
        session.add(krabs)
        # 查询session状态
        print(session.new)

        # 提交事物
        session.commit()

        print(squidward.id)
        print(krabs.id)

def query_by_pk():
    """
    从标识映射中根据主键获取对象
    """
    with Session(engine) as session:
        some_squidward = session.get(User, 1)
        print(some_squidward)

def update():
    with Session(engine) as session:
        sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()

        print(sandy)
        # 改变属性
        sandy.fullname = "Sandy Squirrel"

        # 该对象出现在名为的集合中Session.dirty，表明该对象是“脏的”
        print(sandy in session.dirty)

        # 执行查询，SELECT 之前会自动刷新
        sandy_fullname = session.execute(select(User.fullname).where(User.id == 2)).scalar_one()
        print(sandy_fullname)

        print(sandy_fullname in session.dirty)

        # 未提交事物，本次修改不会永久存储
        session.rollback()

        # 查看sandy内部状态，是过期的
        print(sandy.__dict__)

        # 再次访问属性，会重新执行select
        print(sandy.fullname)

        # 查看sandy内部状态，是有数据的
        print(sandy.__dict__)


def delete():
    with Session(engine) as session:
        patrick = session.get(User, 3)
        # 标记为删除
        session.delete(patrick)

        print(patrick in session)

        # patrick对象还保持Session，我们执行select来自动刷新
        session.execute(select(User).where(User.name == "patrick")).first()

        # 执行自动刷新后，patrick不在session中了
        print(patrick in session)

        # 未提交事物，本次修改不会永久存储

def relationship():
    with Session(engine) as session:

        u1 = User(name="pkrabs", fullname="Pearl Krabs")
        # 打印addresses属性
        print(u1.addresses)

        # 创建Address对象并赋值到User对象
        a1 = Address(email_address="pearl.krabs@gmail.com")
        u1.addresses.append(a1)

        # 打印addresses属性
        print(u1.addresses)
        # 打印Address的user属性，发现互相关联
        print(a1.user)

        # 另一种方式，不显式添加到User的addresses属性
        a2 = Address(email_address="pearl@aol.com", user=u1)
        # 打印addresses属性，发现仍然关联
        print(u1.addresses)

        # 将User实例添加到session
        session.add(u1)

        session.add(u1)
        # 所有对象都在session中
        print(u1 in session)
        print(a1 in session)
        print(a2 in session)

        # 打印id
        print(u1.id)
        print(a1.user_id)

        # 提交事物
        session.commit()

        # 加载id
        print(u1.id)
        # 加载address
        print(u1.addresses)

def join():
    """
    利用relationship()，自动推断on连接条件
    """
    print(select(Address.email_address).select_from(User).join(User.addresses))

    print(select(Address.email_address).join_from(User, Address))

def selectinload():
    """
    加载器策略

    """
    from sqlalchemy.orm import selectinload

    for user_obj in session.execute(
        select(User).options(selectinload(User.addresses))
    ).scalars():
        user_obj.addresses  # access addresses collection already loaded

    
    stmt = select(User).options(selectinload(User.addresses)).order_by(User.id)
    for row in session.execute(stmt):
        print(
            f"{row.User.name}  ({', '.join(a.email_address for a in row.User.addresses)})"
        )

def joinedload():
    from sqlalchemy.orm import joinedload
    stmt = (
        select(Address)
        .options(joinedload(Address.user, innerjoin=True))
        .order_by(Address.id)
    )
    for row in session.execute(stmt):
        print(f"{row.Address.email_address} {row.Address.user.name}")

def where():
    print(select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants"))
    stmt = select(User).where(User.name == "spongebob")
    with Session(engine) as session:
        for row in session.execute(stmt):
            print(row)

def select():
    print(select(User))
    with Session(engine) as session:
        row = session.execute(select(User)).first()
        print(row)
        print(row[0])

def select2():
    with Session(engine) as session:
        user = session.scalars(select(User)).first()
        print(user)

def select3():
    with Session(engine) as session:
        print(select(User.name, User.fullname))

        row = session.execute(select(User.name, User.fullname)).first()
        print(row)

def order_by():
    with Session(engine) as session:
        session.execute(
            select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
        ).all()

        # orderby
        print(select(User).order_by(User.fullname.desc()))


def and_or():
    # “AND” 和 “OR” 连接词
    from sqlalchemy import and_, or_
    print(
        select(Address.email_address).where(
            and_(
                or_(User.name == "squidward", User.name == "sandy"),
                Address.user_id == User.id,
            )
        )
    )

def group_by():
    # 使用 GROUP BY / HAVING 进行聚合函数
    with engine.connect() as conn:
        result = conn.execute(
            select(User.name, func.count(Address.id).label("count"))
            .join(Address)
            .group_by(User.name)
            .having(func.count(Address.id) > 1)
        )
        print(result.all())

    from sqlalchemy import func, desc
    stmt = (
        select(Address.user_id, func.count(Address.id).label("num_addresses"))
        .group_by("user_id")
        .order_by("user_id", desc("num_addresses"))
    )
    print(stmt)

def alias():
    # 使用别名
    from sqlalchemy.orm import aliased
    address_alias_1 = aliased(Address)
    address_alias_2 = aliased(Address)
    print(
        select(User)
        .join_from(User, address_alias_1)
        .where(address_alias_1.email_address == "patrick@aol.com")
        .join_from(User, address_alias_2)
        .where(address_alias_2.email_address == "patrick@gmail.com")
    )

def sbu_query():
    from sqlalchemy.orm import aliased
    subq = select(Address).where(~Address.email_address.like("%@aol.com")).subquery()
    address_subq = aliased(Address, subq)
    stmt = (
        select(User, address_subq)
        .join_from(User, address_subq)
        .order_by(User.id, address_subq.id)
    )
    with Session(engine) as session:
        for user, address in session.execute(stmt):
            print(f"{user} {address}")

def cte():
    cte_obj = select(Address).where(~Address.email_address.like("%@aol.com")).cte()
    address_cte = aliased(Address, cte_obj)
    stmt = (
        select(User, address_cte)
        .join_from(User, address_cte)
        .order_by(User.id, address_cte.id)
    )
    with Session(engine) as session:
        for user, address in session.execute(stmt):
            print(f"{user} {address}")

def union_all():
    stmt1 = select(User).where(User.name == "sandy")
    stmt2 = select(User).where(User.name == "spongebob")
    u = union_all(stmt1, stmt2)

    orm_stmt = select(User).from_statement(u)
    with Session(engine) as session:
        for obj in session.execute(orm_stmt).scalars():
            print(obj)

    user_alias = aliased(User, u.subquery())
    orm_stmt = select(user_alias).order_by(user_alias.id)
    with Session(engine) as session:
        for obj in session.execute(orm_stmt).scalars():
            print(obj)