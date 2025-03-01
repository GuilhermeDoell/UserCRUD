from pymongo import MongoClient
from config import MONGO_URI

class DatabaseService:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client["my_database"]
            print("MongoDB connected successfully!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close_connection(self):
        self.client.close()