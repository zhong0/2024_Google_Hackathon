from pymongo import MongoClient

class ClothesDao:
    def __init__(self, uri, username, password, db_name, collection_name):
        self.client = MongoClient(uri, username=username, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_all_clothes_info(self, username):
        pipeline = [
            {"$unwind": "$clothes"},
            {"$match": {"username": username}},  
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
        return str(list(self.collection.aggregate(pipeline)))

    def get_all_distinct_style(self, username):
        pipeline = [
            {"$match": {"username": username}},  
            {"$unwind": "$clothes"},  
            {"$unwind": "$clothes.detail.style"},  
            {"$project": {"style": {"$toLower": "$clothes.detail.style"}}},  
            {"$group": {"_id": "$style"}},  
            {"$project": {"style": "$_id", "_id": 0}}  
        ]
        results = list(self.collection.aggregate(pipeline))
        return [result['style'] for result in results]  

    def get_all_distinct_occasion(self, username):
        pipeline = [
            {"$match": {"username": username}},
            {"$unwind": "$clothes"},
            {"$project": {"occasion": {"$split": ["$clothes.occasion", ", "]}}},
            {"$unwind": "$occasion"},
            {"$project": {"occasion": {"$toLower": "$occasion"}}},
            {"$group": {"_id": None, "distinct_occasions": {"$addToSet": "$occasion"}}},
            {"$project": {"_id": 0, "distinct_occasions": 1}}
        ]
        results = list(self.collection.aggregate(pipeline))
        if results:
            return results[0]['distinct_occasions']
        else:
            return []

    def get_all_distinct_occasion(self, username):
        pipeline = [
            {"$match": {"username": username}},
            {"$unwind": "$clothes"},
            # Conditionally add a field to handle both strings and arrays
            {"$addFields": {
                "occasions": {
                    "$cond": {
                        "if": {"$isArray": "$clothes.occasion"},
                        "then": "$clothes.occasion",
                        "else": {"$split": ["$clothes.occasion", ", "]}
                    }
                }
            }},
            {"$unwind": "$occasions"},
            {"$project": {"occasion": {"$toLower": "$occasions"}}},
            {"$group": {"_id": None, "distinct_occasions": {"$addToSet": "$occasion"}}},
            {"$project": {"_id": 0, "distinct_occasions": 1}}
        ]
        results = list(self.collection.aggregate(pipeline))
        if results:
            return results[0]['distinct_occasions']
        else:
            return []


    def get_all_distinct_filename(self, username):
        pipeline = {
            "username": username,
            "clothes.filename": {"$ne": None}
        }
        return self.collection.distinct("clothes.filename",  pipeline)
    
    def get_filename_by_category(self, username, category):
        pipeline = {
            "username": username,
            "clothes.category": category,
            "clothes.filename": {"$nin": [None, ""]}
        }
        return self.collection.distinct("clothes.filename", pipeline)
        
    def get_style_by_filename(self, username, filename):
        pipeline = [
            {"$unwind": "$clothes"},
            {"$match": {"clothes.filename": filename}},
            {"username": username},
            {"$project": {"style": "$clothes.detail.style"}}
        ]
        return list(self.collection.aggregate(pipeline))

    def __del__(self):
        self.client.close()
