from pymongo import MongoClient
from pymongo.errors import PyMongoError

class AuthDao:
    def __init__(self, uri, username, password, db_name, collection_name):
        self.client = MongoClient(uri, username=username, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_account(self, username, password):
        if self.is_username_registered(username):
            return False
        try:
            self.collection.insert_one({"username": username, "password": password})
            return True
        except PyMongoError as e:
            print(f"Database error: {e}")
            return False

    def is_username_registered(self, username):
        user = self.collection.find_one({"username": username})
        return user is not None

    def get_hashed_password(self, username):
        user = self.collection.find_one({"username": username})
        if user:
            return user["password"]
        return None

    def __del__(self):
        self.client.close()
