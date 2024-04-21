from pymongo import MongoClient
from pymongo.errors import PyMongoError

class RecommendHistoryDao:
    def __init__(self, uri, username, password, db_name, collection_name):
        self.client = MongoClient(uri, username=username, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_history_recommend(self, username, recommendSet):
        try:
            self.collection.delete_many({'username': username})
            result = self.collection.insert_one({'username': username, 'recommends': recommendSet})
            return result.acknowledged  
        except PyMongoError:
            return False  

    def get_all_history_recommend(self, username):
        try:
            result = self.collection.find_one({'username': username})
            return result['recommends'] if result else []
        except PyMongoError:
            return False

    def insert_history_recommend(self, username, recommendSet):
        try:
            result = self.collection.update_one(
                {'username': username},
                {'$push': {'recommends': recommendSet}}
            )
            return result.modified_count > 0  
        except PyMongoError:
            return False

    def remove_history_recommend(self, username):
        try:
            result = self.collection.delete_many({'username': username})
            return result.deleted_count > 0 
        except PyMongoError:
            return False

    def __del__(self):
        self.client.close()
