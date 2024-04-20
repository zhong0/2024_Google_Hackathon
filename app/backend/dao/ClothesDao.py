from pymongo import MongoClient
import utils.Const as const

class ClothesDao:
    def __init__(self, uri, username, password, db_name, collection_name):
        self.client = MongoClient(uri, username=username, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_all_clothes_info(self):
        pipeline = [
            {"$unwind": "$clothes"},
            {"$project": {
                "name": "$clothes.name",
                "uuid": "$clothes.uuid",
                "category": "$clothes.category",
                "gender": "$clothes.gender",
                "warmth": "$clothes.warmth",
                "details": "$clothes.detail",
                "description": "$clothes.description",
                "occasion": "$clothes.occasion",
                "filename": "$clothes.filename"
            }}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_all_distinct_style(self, username):
        return self.collection.distinct("clothes.detail.style")

    def get_all_distinct_scenario(self, username):
        return self.collection.distinct("clothes.occasion")

    def get_all_distinct_category(self, username):
        return self.collection.distinct("clothes.category")

    def get_all_distinct_filename(self, username):
        return self.collection.distinct("clothes.filename")

    def get_style_by_filename(self, username, filename):
        pipeline = [
            {"$unwind": "$clothes"},
            {"$match": {"clothes.filename": filename}},
            {"$project": {"style": "$clothes.detail.style"}}
        ]
        return list(self.collection.aggregate(pipeline))

    def __del__(self):
        self.client.close()
