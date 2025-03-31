import mysql.connector
from common.config import MYSQL_CONFIG

# 数据库连接信息
db_config = {
    'host': 'localhost',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database',
    'charset': 'utf8mb4'
}

try:
    # 建立连接
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor(dictionary=True) # 返回字典形式的结果

    # 插入数据
    sql_insert = "INSERT INTO users (name, age) VALUES (%s, %s)"
    values_insert = ('Alice', 30)
    cursor.execute(sql_insert, values_insert)
    connection.commit()

    # 查询数据
    sql_select = "SELECT * FROM users WHERE age > %s"
    values_select = (25,)
    cursor.execute(sql_select, values_select)
    results = cursor.fetchall()
    print("查询结果:", results)

    # 修改数据
    sql_update = "UPDATE users SET age = %s WHERE name = %s"
    values_update = (35, 'Alice')
    cursor.execute(sql_update, values_update)
    connection.commit()

    # 删除数据
    sql_delete = "DELETE FROM users WHERE name = %s"
    values_delete = ('Alice',)
    cursor.execute(sql_delete, values_delete)
    connection.commit()

except mysql.connector.Error as e:
    print(f"数据库操作出错: {e}")
    if connection:
        connection.rollback() #如果出现错误，回滚事务，确保数据一致性

finally:
    # 关闭连接
    if connection:
        cursor.close()
        connection.close()