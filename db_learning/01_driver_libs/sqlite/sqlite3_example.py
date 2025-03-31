import sqlite3
from common.config import SQLITE_CONFIG

try:
    connection = sqlite3.connect(SQLITE_CONFIG['database'])
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Eve', 29)")
    connection.commit()

    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("查询结果:", results)

except sqlite3.Error as e:
    print(f"数据库操作出错: {e}")
    if connection:
        connection.rollback()
finally:
    if connection:
        cursor.close()
        connection.close()