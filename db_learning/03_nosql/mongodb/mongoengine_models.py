# 03_nosql/mongodb/mongoengine_models.py

from mongoengine import Document, StringField, IntField, DateTimeField, connect
from common.config import MONGOENGINE_CONFIG
import datetime

# 连接到 MongoDB
connect(MONGOENGINE_CONFIG['database'], host=MONGOENGINE_CONFIG['host'], port=MONGOENGINE_CONFIG['port'])

SEX_CHOICES = (
    ('male', '男'),
    ('female', '女'),
)

class User(Document):
    name = StringField(required=True, max_length=32)
    age = IntField()
    sex = StringField(required=True, choices=SEX_CHOICES)
    email = StringField()
    created_at = DateTimeField(default=datetime.now())

    meta = {'collection': 'users'}  # 指定集合名称