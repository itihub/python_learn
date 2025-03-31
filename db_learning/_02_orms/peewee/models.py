# 02_orms/peewee/models.py

from peewee import *
from common.config import SQLITE_CONFIG

db = SqliteDatabase(SQLITE_CONFIG['database'])

class User(Model):
    name = CharField()
    age = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([User])