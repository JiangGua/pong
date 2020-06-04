import os
import pymongo

DATABASE_NAME = os.environ.get('DATABASE_NAME', default='pong')
MONGO_URI = os.environ.get('MONGO_URI', default='mongodb://localhost:27017/pong')

db = pymongo.MongoClient(MONGO_URI, connect = False)[DATABASE_NAME]
db_links = db['links']
