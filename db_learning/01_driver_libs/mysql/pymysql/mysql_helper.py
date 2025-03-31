import pymysql

class MySQLHelper:
    def __init__(self, **db_config):
        self.db_config = db_config
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = pymysql.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            return True
        except pymysql.MySQLError as e:
            print(f"数据库连接出错: {e}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, sql, values=None):
        try:
            self.cursor.execute(sql, values)
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"查询出错: {e}")
            return None

    def execute_non_query(self, sql, values=None):
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"非查询操作出错: {e}")
            if self.connection:
                self.connection.rollback()
            return False

# 使用示例
db = MySQLHelper(**db_config)
if db.connect():
    results = db.execute_query("SELECT * FROM users")
    if results:
        print("查询结果:", results)
    db.execute_non_query("INSERT INTO users (name, age) VALUES (%s, %s)", ('Bob', 28))
    db.close()