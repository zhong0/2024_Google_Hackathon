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
                "detail": "$clothes.detail",
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
                "detail": "$clothes.detail",
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
                "detail": "$clothes.detail",
                "description": "$clothes.description",
                "occasion": "$clothes.occasion",
                "filename": "$clothes.filename",
                "_id": 0
            }}
        ]
        clothes_info_list = list(self.collection.aggregate(pipeline))
        return clothes_info_list
    
    def get_clothes_sale_info_by_filename(self, username, filename):
        if not filename:
            return None

        pipeline = [
            {"$match": {"username": username}},
            {"$unwind": "$clothes"},
            {"$match": {"clothes.filename": filename}},
            {"$project": {
                "username": "$username",
                "name": "$clothes.name",
                "url": "$clothes.url",
                "sale_info": "$clothes.sale_info",
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
    
    def remove_sale_clothes(self, username, filename):

        result = self.collection.update_one(
            {"username": username}, 
            {"$pull": {"clothes": {"filename": filename}}}  
        )
        
        if result.modified_count > 0:
            return True
        else:
            return False
        
    def clothes_on_sale(self, username, clothes_info):
        # 首先检查用户是否存在
        user_exists = self.collection.find_one({"username": username})

        if not user_exists:
            # 如果用户不存在，插入新用户和其衣物信息
            new_user_data = {
                "username": username,
                "clothes": [clothes_info]
            }
            result = self.collection.insert_one(new_user_data)
        else:
            # 如果用户已存在，检查指定的 filename 是否已经存在于衣物列表中
            clothes_exist = self.collection.find_one({
                "username": username,
                "clothes": {"$elemMatch": {"filename": clothes_info['filename']}}
            })
            
            if clothes_exist:
                # 如果衣物已存在，更新这条衣物信息
                result = self.collection.update_one(
                    {"username": username, "clothes.filename": clothes_info['filename']},
                    {"$set": {"clothes.$": clothes_info}}
                )
            else:
                # 如果衣物不存在，添加新的衣物信息到数组
                result = self.collection.update_one(
                    {"username": username},
                    {"$push": {"clothes": clothes_info}}
                )

        return result.acknowledged
    
    def get_all_distinct_category(self, username):
        pipeline = [
            {"$match": {"username": username}},
            {"$unwind": "$clothes"},
            {"$project": {"category": {"$toLower": "$clothes.category"}}},
            {"$group": {"_id": None, "distinct_categories": {"$addToSet": "$category"}}},
            {"$project": {"_id": 0, "distinct_categories": 1}}
        ]
        results = list(self.collection.aggregate(pipeline))
        if results:
            return results[0]['distinct_categories']
        else:
            return []

    def get_filename_by_category(self, username, category):
        pipeline = [
            {"$match": {"username": username}}, 
            {"$unwind": "$clothes"}, 
            {"$match": {"clothes.category": category, "clothes.filename": {"$nin": [None, ""]}}}, 
            {"$project": {"filename": "$clothes.filename"}}
        ]
        
        results = self.collection.aggregate(pipeline)
        filenames = [result['filename'] for result in results if 'filename' in result]
        return filenames

  
        
