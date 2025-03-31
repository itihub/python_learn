# Django ORM 学习

本目录包含使用 Django ORM 框架连接和操作数据库的示例代码。

## 学习目标

* 掌握 Django ORM 的模型定义。
* 学习如何使用 Django ORM 进行 CRUD 操作。
* 理解 Django ORM 的查询构建和关系映射。
* 了解 Django 的视图和 URL 路由。

## 文件说明

* `models.py`: Django 模型定义。
* `views.py`: Django 视图（数据库操作）。
* `settings.py`: django配置文件。
* `urls.py`: django urls配置文件。

## 使用说明

1.  确保已安装 `django` 库：

    ```bash
    pip install django
    ```

2.  修改 `common/config.py` 文件中的数据库连接信息。
3.  运行 Django 服务器：

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

4.  通过浏览器或 HTTP 客户端访问 API。

## 学习资源

* Django ORM 官方文档：[https://docs.djangoproject.com/en/stable/topics/db/models/](https://docs.djangoproject.com/en/stable/topics/db/models/)