import pymysql
from common.config import MYSQL_CONFIG

# 数据库连接信息
db_config = {
    'host': 'localhost',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor  # 返回字典形式的结果
}

try:
    """
    使用 pymysql 创建的连接可以获取多个游标。每个游标都独立于其他游标，允许你同时执行多个查询或操作。
    pymysql 提供了不同类型的游标，例如 DictCursor（返回字典形式的结果）和默认游标（返回元组形式的结果）。
    对于查询语句，使用游标的 fetchone()、fetchall() 或 fetchmany() 方法获取查询结果。
    对于修改数据的操作，使用连接对象的 commit() 方法提交事务，或使用 rollback() 方法回滚事务。
    """

    # 建立连接：使用驱动程序提供的连接函数，传入数据库的连接参数来建立与数据库的连接。
    connection = pymysql.connect(**MYSQL_CONFIG)
    # 创建游标：通过连接对象创建一个游标（cursor）对象。游标用于执行 SQL 语句。
    cursor = connection.cursor()

    # 插入数据
    sql_insert = "INSERT INTO users (name, age) VALUES (%s, %s)"
    values_insert = ('Alice', 30)
    # 使用游标的 execute() 方法执行 SQL 
    cursor.execute(sql_insert, values_insert)
    connection.commit()

    # 查询数据
    sql_select = "SELECT * FROM users WHERE age > %s"
    values_select = (25,)
    # 使用游标的 execute() 方法执行 SQL 
    cursor.execute(sql_select, values_select)
    # 获取结果：对于查询语句，使用游标的 fetchone()、fetchall() 或 fetchmany() 方法获取查询结果。
    results = cursor.fetchall()
    print("查询结果:", results)

    # 修改数据
    sql_update = "UPDATE users SET age = %s WHERE name = %s"
    values_update = (35, 'Alice')
    # 使用游标的 execute() 方法执行 SQL 
    cursor.execute(sql_update, values_update)
    connection.commit()

    # 删除数据
    sql_delete = "DELETE FROM users WHERE name = %s"
    values_delete = ('Alice',)
    cursor.execute(sql_delete, values_delete)
    connection.commit()

except pymysql.MySQLError as e:
    print(f"数据库操作出错: {e}")
    if connection:
        connection.rollback() #如果出现错误，回滚事务，确保数据一致性

finally:
    # 释放资源
    if connection:
        # 关闭游标
        cursor.close()
        # 关闭连接
        connection.close()