"""
SQLAlchemy Core 和 ORM 的核心元素是 SQL 表达式语言，
它允许流畅、可组合地构建 SQL 查询。这些查询的基础是 Python 对象，它们表示数据库概念（如表和列）。
这些对象统称为数据库元数据。
"""
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, insert, select, bindparam, func, cast, text
from sqlalchemy import MetaData
from db_learning.common.config import MYSQL_CONFIG


metadata_obj = MetaData()

#  建立连接-数据库引擎
DATABASE_URL = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}?charset={MYSQL_CONFIG['charset']}"
engine = create_engine(
    DATABASE_URL,
    echo=True,  # echo 设为 True 会打印出实际执行的 sql，调试的时候更方便
    future=True,  # 使用 SQLAlchemy 2.0 API，向后兼容
    pool_size=5, # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
    pool_recycle=3600, # 设置时间以限制数据库自动断开  
)


"""
组件Table
Table用 Python 编写的构造与 SQL CREATE TABLE 语句相似；
从表名开始，然后列出每一列，其中每列都有一个名称和数据类型。
"""
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(30)),
)

# 打印数据表中指定的列
print(user_table.c.name)
print(user_table.c.fullname)

# 打印数据表中所有的列
print(user_table.c.keys())

# 打印数据表中的主键
print(user_table.primary_key)


address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    # 外键
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(255), nullable=False),
)

def create_dll():
    # 向数据库发送CREATE DDL语句
    metadata_obj.create_all(engine)

def drop_dll():
    # 向数据库发送DROP DDL语句
    metadata_obj.drop_all(engine)

def insert1():
    # 使用insert()函数生成 SQL INSERT 语句
    print("使用insert()函数生成 SQL INSERT 语句")
    print("-------------------------------------")
    # 显式创建 SQL INSERT 语句的 VALUES 子句
    stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
    print(stmt)
    compiled = stmt.compile()
    print(compiled.params)

    # 执行语句
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
        # 打印主键值
        print(result.inserted_primary_key)

def insert2():
    # 自动生成“values”子句
    print(insert(user_table))
    with engine.connect() as conn:
        result = conn.execute(
            insert(user_table),
            [
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"},
            ],
        )
        conn.commit()

def insert3():
    """
    insert 结合 select 子句
    """
    # select 子句
    scalar_subq = (
        select(user_table.c.id)
        .where(user_table.c.name == bindparam("username"))
        .scalar_subquery()
    )

    with engine.connect() as conn:
        result = conn.execute(
            insert(address_table).values(user_id=scalar_subq),
            [
                {
                    "username": "spongebob",
                    "email_address": "spongebob@sqlalchemy.org",
                },
                {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
                {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
            ],
        )
        conn.commit()

def insert4():
    # insert不带任何参数，则会生成一个真正的“空” INSERT，它只插入表的“默认值”
    print(insert(user_table).values().compile(engine))

def insert5():
    # 插入并返回
    insert_stmt = insert(address_table).returning(
        address_table.c.id, address_table.c.email_address
    )
    print(insert_stmt)

def insert6():
    # 插入结合select
    select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
    insert_stmt = insert(address_table).from_select(
        ["user_id", "email_address"], select_stmt
    )
    print(insert_stmt)
    print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))


def select1():
    # 使用select()函数生成 SQL SELECT 语句
    stmt = select(user_table).where(user_table.c.name == "spongebob")
    print(stmt)

    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)

def select2():
    print(select(user_table))

def select3():
    print(select(user_table.c.name, user_table.c.fullname))

def select4():
    print(select(user_table.c["name", "fullname"]))

def select5():
    stmt = select(
        ("Username: " + user_table.c.name).label("username"),
    ).order_by(user_table.c.name)

    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"{row.username}")

def select6():
# 制造一个硬编码字符串文字并将其嵌入 SELECT 语句中
    stmt = select(text("'some phrase'"), user_table.c.name).order_by(user_table.c.name)

    with engine.connect() as conn:
        print(conn.execute(stmt).all())

def select7():
    from sqlalchemy import literal_column
    stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(
        user_table.c.name
    )
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"{row.p}, {row.name}")

def where1():
    # WHERE 子句
    print(user_table.c.name == "squidward")

    print(address_table.c.user_id > 10)

def select_where1():
    # 传递给Select.where()方法来生成 WHERE 子句
    print(select(user_table).where(user_table.c.name == "squidward"))

def select_where2():
    # 生成由 AND 连接的多个表达式，Select.where() 可以调用该方法任意次
    print(
        select(address_table.c.email_address)
        .where(user_table.c.name == "squidward")
        .where(address_table.c.user_id == user_table.c.id)
    )

def select_where3():
    # 一次调用Select.where()也可以接受多个表达式，效果相同：
    print(
        select(address_table.c.email_address).where(
            user_table.c.name == "squidward",
            address_table.c.user_id == user_table.c.id,
        )
    )

def join1():
    print(select(user_table.c.name))
    print(select(user_table.c.name, address_table.c.email_address))

def join2():
    # 连表查询，指示 JOIN 的左侧和右侧，ON 子句自动推断
    print(
        select(user_table.c.name, address_table.c.email_address).join_from(
            user_table, address_table
        )
    )

def join3():
    # 连表查询，只指示 JOIN 的右侧，推断左侧，ON 子句自动推断
    print(select(user_table.c.name, address_table.c.email_address).join(address_table))

def join4():
    # 连表查询，显式添加到 FROM 子句中
    print(select(address_table.c.email_address).select_from(user_table).join(address_table))

def join5():
    # 连表查询，设置 ON 子句
    print(
        select(address_table.c.email_address)
        .select_from(user_table)
        .join(address_table, user_table.c.id == address_table.c.user_id)
    )

def join6():
    # 连表查询指定连接方式，OUTER 和 FULL 连接
    print(select(user_table).join(address_table, isouter=True))
    print(select(user_table).join(address_table, full=True))

def orderby1():
    # orderby
    print(select(user_table).order_by(user_table.c.name))

def from1():
    # 使用SQL函数查询
    from sqlalchemy import func
    print(select(func.count("*")).select_from(user_table))


def func1():
    # 使用 GROUP BY / HAVING 进行聚合函数
    from sqlalchemy import func
    # 实例Function
    count_fn = func.count(user_table.c.id)
    print(count_fn)

def alias():
    # 使用别名
    user_alias_1 = user_table.alias()
    user_alias_2 = user_table.alias()
    print(
        select(user_alias_1.c.name, user_alias_2.c.name).join_from(
            user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id
        )
    )

def sub_query1():
    # 子查询和 CTE
    subq = (
        select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
        .group_by(address_table.c.user_id)
        .subquery()
    )
    print(subq)

    # 获取子查询列名
    print(select(subq.c.user_id, subq.c.count))

def sub_query2():
    subq = (
        select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
        .group_by(address_table.c.user_id)
        .subquery()
    )
    stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
        user_table, subq
    )

    print(stmt)

def cte1():
    """
    CTE实际上与构造的使用方式相同Subquery
    通过更改方法的调用Select.subquery()以改为使用 Select.cte()
    """
    subq = (
        select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
        .group_by(address_table.c.user_id)
        .cte()
    )

    stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
        user_table, subq
    )

    print(stmt)

def scalar_subquery():
    """
    标量子查询是返回恰好零行或一行和恰好一列的子查询。然后，
    子查询用于封闭 SELECT 语句的 COLUMNS 或 WHERE 子句中，
    与常规子查询的不同之处在于它不在 FROM 子句中使用
    """
    subq = (
        select(func.count(address_table.c.id))
        .where(user_table.c.id == address_table.c.user_id)
        .scalar_subquery()
    )
    print(subq)

    print(subq == 5)

    stmt = select(user_table.c.name, subq.label("address_count"))
    print(stmt)

def scalar_subquery2():
    stmt = (
        select(
            user_table.c.name,
            address_table.c.email_address,
            subq.label("address_count"),
        )
        .join_from(user_table, address_table)
        .order_by(user_table.c.id, address_table.c.id)
    )
    print(stmt)

    subq = (
        select(func.count(address_table.c.id))
        .where(user_table.c.id == address_table.c.user_id)
        .scalar_subquery()
        .correlate(user_table)
    )

    with engine.connect() as conn:
        result = conn.execute(
            select(
                user_table.c.name,
                address_table.c.email_address,
                subq.label("address_count"),
            )
            .join_from(user_table, address_table)
            .order_by(user_table.c.id, address_table.c.id)
        )
        print(result.all())

def union_all():
    from sqlalchemy import union_all
    stmt1 = select(user_table).where(user_table.c.name == "sandy")
    stmt2 = select(user_table).where(user_table.c.name == "spongebob")
    u = union_all(stmt1, stmt2)
    with engine.connect() as conn:
        result = conn.execute(u)
        print(result.all())

    u_subq = u.subquery()
    stmt = (
        select(u_subq.c.name, address_table.c.email_address)
        .join_from(address_table, u_subq)
        .order_by(u_subq.c.name, address_table.c.email_address)
    )
    with engine.connect() as conn:
        result = conn.execute(stmt)
        print(result.all())

def exists():
    subq = (
        select(func.count(address_table.c.id))
        .where(user_table.c.id == address_table.c.user_id)
        .group_by(address_table.c.user_id)
        .having(func.count(address_table.c.id) > 1)
    ).exists()
    with engine.connect() as conn:
        result = conn.execute(select(user_table.c.name).where(subq))
        print(result.all())

def not_exists():
    subq = (
        select(address_table.c.id).where(user_table.c.id == address_table.c.user_id)
    ).exists()
    with engine.connect() as conn:
        result = conn.execute(select(user_table.c.name).where(~subq))
        print(result.all())

def func_count():
    print(select(func.count()).select_from(user_table))

def func_lower():
    print(select(func.lower("A String With Much UPPERCASE")))

def func_now():
    stmt = select(func.now())
    with engine.connect() as conn:
        result = conn.execute(stmt)
        print(result.all())

def func_json():
    from sqlalchemy import JSON
    function_expr = func.json_object('{a, 1, b, "def", c, 3.5}', type_=JSON)

    stmt = select(function_expr["def"])
    print(stmt)

def cast():
    """
    类型转换
    """
    from sqlalchemy import cast
    stmt = select(cast(user_table.c.id, String))
    with engine.connect() as conn:
        result = conn.execute(stmt)
        result.all()

    from sqlalchemy import JSON
    print(cast("{'a': 'b'}", JSON)["a"])

def update():
    from sqlalchemy import update
    stmt = (
        update(user_table)
        .where(user_table.c.name == "patrick")
        .values(fullname="Patrick the Star")
    )
    print(stmt)

def update2():
    stmt = update(user_table).values(fullname="Username: " + user_table.c.name)
    print(stmt)

def update3():
    from sqlalchemy import bindparam
    stmt = (
        update(user_table)
        .where(user_table.c.name == bindparam("oldname"))
        .values(name=bindparam("newname"))
    )
    with engine.begin() as conn:
        conn.execute(
            stmt,
            [
                {"oldname": "jack", "newname": "ed"},
                {"oldname": "wendy", "newname": "mary"},
                {"oldname": "jim", "newname": "jake"},
            ],
        )

def update4():
    scalar_subq = (
        select(address_table.c.email_address)
        .where(address_table.c.user_id == user_table.c.id)
        .order_by(address_table.c.id)
        .limit(1)
        .scalar_subquery()
    )
    update_stmt = update(user_table).values(fullname=scalar_subq)
    print(update_stmt)

def update_from():
    update_stmt = (
        update(user_table)
        .where(user_table.c.id == address_table.c.user_id)
        .where(address_table.c.email_address == "patrick@aol.com")
        .values(fullname="Pat")
    )
    print(update_stmt)

def update_from2():
    update_stmt = (
        update(user_table)
        .where(user_table.c.id == address_table.c.user_id)
        .where(address_table.c.email_address == "patrick@aol.com")
        .values(
            {
                user_table.c.fullname: "Pat",
                address_table.c.email_address: "pat@aol.com",
            }
        )
    )
    from sqlalchemy.dialects import mysql
    print(update_stmt.compile(dialect=mysql.dialect()))

# def update5():
#     update_stmt = update(some_table).ordered_values(
#         (some_table.c.y, 20), (some_table.c.x, some_table.c.y + 10)
#     )
#     print(update_stmt)

def delete1():
    from sqlalchemy import delete
    stmt = delete(user_table).where(user_table.c.name == "patrick")
    print(stmt)

def delete2():
    from sqlalchemy import delete
    delete_stmt = (
        delete(user_table)
        .where(user_table.c.id == address_table.c.user_id)
        .where(address_table.c.email_address == "patrick@aol.com")
    )
    from sqlalchemy.dialects import mysql
    print(delete_stmt.compile(dialect=mysql.dialect()))

def delete3():
    with engine.begin() as conn:
        result = conn.execute(
            update(user_table)
            .values(fullname="Patrick McStar")
            .where(user_table.c.name == "patrick")
        )
        print(result.rowcount)

def update_return():
    with engine.begin() as conn:
        result = conn.execute(
            update(user_table)
            .values(fullname="Patrick McStar")
            .where(user_table.c.name == "patrick")
        )
        print(result.rowcount)

def delete_return():
    from sqlalchemy import delete
    delete_stmt = (
        delete(user_table)
        .where(user_table.c.name == "patrick")
        .returning(user_table.c.id, user_table.c.name)
    )
    print(delete_stmt)