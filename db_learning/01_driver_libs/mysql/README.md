# MySQL 驱动程序库学习

本目录包含使用 Python 驱动程序库（`pymysql` 和 `mysql-connector-python`）连接和操作 MySQL 数据库的示例代码。

## 学习目标

* 掌握 `pymysql` 和 `mysql-connector-python` 库的安装和使用。
* 理解如何建立 MySQL 数据库连接。
* 学习如何使用 SQL 语句进行 CRUD 操作（创建、读取、更新、删除）。
* 掌握如何处理数据库事务。
* 了解如何封装数据库操作，提高代码的可重用性。

## 文件说明

* `pymysql_example.py`: 使用 `pymysql` 库的简单示例。
* `mysql_connector_example.py`: 使用 `mysql-connector-python` 库的简单示例。
* `mysql_helper.py`: 封装了常用 MySQL 操作的辅助类。

## 使用说明

1.  确保已安装 `pymysql` 和 `mysql-connector-python` 库：

    ```bash
    pip install pymysql mysql-connector-python
    ```

2.  修改 `common/config.py` 文件中的 MySQL 连接信息。
3.  运行示例代码，查看输出结果。

## 学习资源

* `pymysql` 官方文档：[https://pymysql.readthedocs.io/en/latest/](https://pymysql.readthedocs.io/en/latest/)
* `mysql-connector-python` 官方文档：[https://dev.mysql.com/doc/connector-python/en/](https://dev.mysql.com/doc/connector-python/en/)