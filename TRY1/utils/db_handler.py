from pymongo import MongoClient
from ..config.config import MONGODB_URI, DB_NAME, COLLECTION_NAME

class DatabaseHandler:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def save_trends(self, trends_data):
        """Save trends data to MongoDB"""
        return self.collection.insert_one(trends_data)

    def get_all_trends(self):
        """Retrieve all trends from the database"""
        return list(self.collection.find().sort('timestamp', -1))

    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()