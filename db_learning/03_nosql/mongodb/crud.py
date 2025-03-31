# 03_nosql/mongodb/crud.py

from pymongo import MongoClient
from common.config import MONGODB_CONFIG
from bson.objectid import ObjectId
import datetime

# 连接MongoDB
client = MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
# 切换数据库
db = client[MONGODB_CONFIG['database']]

def create_document(collection_name, document):
    collection = db[collection_name]
    result = collection.insert_one(document)
    return result.inserted_id

def read_documents(collection_name, query={}):
    collection = db[collection_name]
    documents = list(collection.find(query))
    return documents

def read_document(collection_name, id):
    collection = db[collection_name]
    document = collection.find_one({'_id': ObjectId(id)})
    return document

def update_document(collection_name, query, update):
    collection = db[collection_name]
    result = collection.update_one(query, {'$set': update})
    return result.modified_count

def update_documents(collection_name, query, update):
    collection = db[collection_name]
    result = collection.update_many(query, {'$set': update})
    return result.modified_count

def delete_document(collection_name, query):
    collection = db[collection_name]
    result = collection.delete_one(query)
    return result.deleted_count

def delete_documents(collection_name, query):
    collection = db[collection_name]
    result = collection.delete_many(query)
    return result.deleted_count

# 示例用法
# create_document('users', {'name': 'Alice', 'age': 30, 'created_at': datetime.now()})
# print(read_documents('users'))
# update_document('users', {'name': 'Alice'}, {'age': 31})
# delete_document('users', {'name': 'Alice'})