from pymongo import MongoClient

class ShopDao:
    def __init__(self, uri, username, password, db_name, collection_name):
        self.client = MongoClient(uri, username=username, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_all_shop_usernames(self):
        shop_usernames = self.collection.find({}, {"username": 1, "_id": 0})
        username_list = [shop['username'] for shop in shop_usernames if 'username' in shop]
        
        return username_list
    
    def get_all_clothes_info_by_shop_list(self, shop_list):
        pipeline = [
            {"$match": {"shop_name": {"$in": shop_list}}},
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
        clothes_list = list(self.collection.aggregate(pipeline))
        return clothes_list
    
    def get_clothes_info_by_filename(self, filename):
        pipeline = [
            {"$unwind": "$clothes"},
            {"$match": {"clothes.filename": filename}},
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
        result = list(self.collection.aggregate(pipeline))
        if result:
            return result[0]
        else:
            return None
