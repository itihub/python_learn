import psycopg2
from common.config import POSTGRES_CONFIG

try:
    connection = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('David', 32)")
    connection.commit()

    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("查询结果:", results)

except psycopg2.Error as e:
    print(f"数据库操作出错: {e}")
    if connection:
        connection.rollback()
finally:
    if connection:
        cursor.close()
        connection.close()