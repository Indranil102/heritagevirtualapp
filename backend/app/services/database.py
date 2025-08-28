import certifi
from pymongo import MongoClient
from app.core.config import settings

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self):
        try:
            self.client = MongoClient(
                settings.MONGODB_URI,
                tlsCAFile=certifi.where(),
                tls=True,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000
            )
            self.db = self.client[settings.MONGODB_DATABASE]
            # Test connection
            self.client.admin.command('ping')
            print("✅ Connected to MongoDB successfully!")
            return True
        except Exception as e:
            print(f"❌ MongoDB connection failed: {str(e)}")
            return False
            
    def close(self):
        if self.client:
            self.client.close()
            
    def get_collection(self, collection_name):
        if self.db:
            return self.db[collection_name]
        return None

# Global database instance
mongodb = MongoDB()