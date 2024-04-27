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
    
    # for explore-outfit & explore-pieces-recommed
    def get_all_shop_clothes_info(self, username):
        pipeline = [
            # Exclude clothes associated with the given username
            {"$match": {"username": {"$ne": username}}},
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
        if not filename:
            return None

        pipeline = [
            {"$match": {"clothes.filename": filename}},
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
                "filename": "$clothes.filename",
                "_id": 0 
            }}
        ]

        try:
            result = list(self.collection.aggregate(pipeline))
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            return None
        
    def get_clothes_filename(self, username):
        pipeline = [
            {"$match": {"username": username}},
            {"$unwind": "$clothes"},
            {"$project": {"filename": "$clothes.filename", "_id": 0}}
        ]
        results = list(self.collection.aggregate(pipeline))
        filename_list = [result['filename'] for result in results if 'filename' in result]
        return str(filename_list)

    def get_clothes_info(self, username):
        pipeline = [
            {"$match": {"username": username}},
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
                "filename": "$clothes.filename",
                "_id": 0
            }}
        ]
        clothes_info_list = list(self.collection.aggregate(pipeline))
        return clothes_info_list