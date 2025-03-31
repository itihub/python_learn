"""
engine.connect() 用于直接从 SQLAlchemy Engine 对象获取一个数据库连接。
使用场景：
    当您需要执行原始 SQL 语句或使用 SQLAlchemy Core 功能时。
    当您需要更精细地控制数据库连接的生命周期时。
    在非 ORM 操作中，例如执行数据迁移或批量数据处理。
"""
from sqlalchemy import (create_engine, text)
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

def test1():
    """
    上下文管理器创建数据库连接并在事务中执行操作。
    Python DBAPI 的默认行为是事务始终处于进行状态；当连接被释放时，将发出 ROLLBACK 以结束事务。事务不会自动提交；
    """
    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())

def test2():
    """
    使用 DBAPI 提交事物
    使用 connection.commit()方法提交事务

    SQLAlchemy 将这种风格称为“随心所欲地提交”。
    """
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()

def test3():
    """
    另一种提交数据的样式。
    使用 Engine.begin()方法来获取连接
    如果执行成功，则在末尾使用 COMMIT，如果引发异常，则使用 ROLLBACK。这种样式称为begin once
    """
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
        )

def test4():
    """
    获取行
    返回的对象被Result称为结果行的可迭代对象。
    Result有很多方法可以获取和转换行，比如Result.all() 前面介绍的方法，它返回所有对象的列表Row。
    对象Row本身的作用类似于 Python 命名元组。下面我们说明了访问行的多种方法。
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))

        # 迭代器（iterator）通常被设计为只能迭代一次

        print("元组赋值访问----------------------------------")
        # 元组赋值访问
        # for x, y in result:
        #     print(f"x: {x}  y: {y}")

        print("索引访问----------------------------------")
        # 索引访问
        # for row in result:
        #     x = row[0]
        #     y = row[1]
        #     print(f"x: {x}  y: {y}")
        
        print("属性名称访问----------------------------------")
        # 属性名称访问
        # for row in result:
        #     print(f"x: {row.x}  y: {row.y}")

        print("映射访问----------------------------------")
        # 映射访问
        for dict_row in result.mappings():
            x = dict_row["x"]
            y = dict_row["y"]
            print(f"x: {x}  y: {y}")
        

def test5():
    """
    发送参数
    text() 构造使用冒号格式“ :y”接受这些参数。
    然后将实际值:y作为第二个参数 connection.execute()以字典的形式传递给
    禁止直接使用字符串拼接SQL,避免 SQL 注入攻击
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

def test6():
    """"
    发送多个参数
    对于“INSERT”、“UPDATE”和“DELETE”等DML语句，
    我们可以通过传递字典列表而不是单个字典来向方法发送多个参数集connection.execute()，
    这表明单个 SQL 语句应该被调用多次，每个参数集调用一次。这种执行方式称为executemany：
    """
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
        )
        conn.commit()
