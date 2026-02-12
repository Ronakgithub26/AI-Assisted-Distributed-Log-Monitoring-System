from pymongo import MongoClient
from config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

logs_collection = db.logs
projects_collection = db.projects

