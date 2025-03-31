# common/config.py

# MySQL 配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'your_mysql_database',
    'charset': 'utf8mb4',
    'cursorclass': 'pymysql.cursors.DictCursor'  # 返回字典形式的结果
}


# PostgreSQL 配置
POSTGRES_CONFIG = {
    'host': 'localhost',
    'user': 'your_postgres_user',
    'password': 'your_postgres_password',
    'database': 'your_postgres_database'
}

# SQLite 配置
SQLITE_CONFIG = {
    'database': 'my_sqlite.db'
}

# MongoDB 配置
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'your_mongodb_database',
}

# Redis 配置
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

# MongoDB 配置 (用于 MongoEngine)
MONGOENGINE_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'mongoengine_db',
}