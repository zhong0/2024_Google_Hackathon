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
        
    def get_style_by_filename(self, username, filename):
        pipeline = [
            {"$unwind": "$clothes"},  
            {"$match": {"clothes.filename": filename, "username": username}}, 
            {"$unwind": "$clothes.detail.style"},  
            {"$group": {"_id": None, "distinct_styles": {"$addToSet": "$clothes.detail.style"}}},  
            {"$project": {"_id": 0, "styles": "$distinct_styles"}} 
        ]
        
        results = list(self.collection.aggregate(pipeline))
        if results and 'styles' in results[0]:
            return results[0]['styles']
        return []  
    
    def get_clothes_info_by_filename(self, username, filename):
        pipeline = [
            {"$match": {"username": username}}, 
            {"$unwind": "$clothes"},  
            {"$match": {"clothes.filename": filename}},  
            {"$project": {  
                "name": "$clothes.name",
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
        
        result = list(self.collection.aggregate(pipeline))
        
        if result:
            return result[0] 
        else:
            return None 
        
    def create_username(self, username):
        username_data = {"username":username, "favorite_set":[], "clothes":[]}

        return self.collection.insert_one(username_data).acknowledged
    
    def insert_clothes_2_username(self, username, clothes_data):
        #check if 1st time upload clothes
        clothes_data_ = self.collection.find({"username":username})
        if len(list(clothes_data_)) == 0:
            clothes_data_ = {"username":username, "favorite_set":[], "clothes":clothes_data}
            result =  self.collection.insert_one(clothes_data_)
        else:
            result =  self.collection.update_one({"username":username}, { "$push": {"clothes": { "$each": clothes_data}}})

        return result.acknowledged

    def is_favorite_set_repeated(self, username, filename_list):
        query = {
                "favorite_set": {
                    "$elemMatch": {
                        "clothes_list": {"$all": filename_list, "$size": len(filename_list)}
                    }
                },
                "username":username
            }
        result = self.collection.find_one(query)
        print(result)
        if result:
            return True
        else:
            return False
    
    def get_favorite_set(self, username):
        user_document = self.collection.find_one({"username": username}, {"favorite_set": 1, "_id": 0})
        if user_document:
            return user_document.get('favorite_set', [])
        else:
            return []
    
    def insert_favorite_set(self, username, filename_list):
        #currently cannot test by swaggerui
        #print(filename_list, len(filename_list))
        clothes_data_ = self.collection.find({"username":username})
        if len(list(clothes_data_)) == 0:
            if self.create_username(username):
                #clothes_data_ = self.collection.find({"username":username})
                result = self.collection.update_one({"username":username}, {"$set": {"favorite_set": [{"set_id": 0, "clothes_list": filename_list}]}})
            else:
                return {"error":"can't create new username"}
        else:
            if not self.is_favorite_set_repeated(username, filename_list):
                result = self.collection.find_one({"username":username})
                id_offset = len(result.get("favorite_set"))
                result = self.collection.update_one({"username":username}, {"$push": {"favorite_set": {"$each": [{"set_id":id_offset, "clothes_list": filename_list}]}}})
            else:
                return False
        return result.acknowledged

    def remove_favorite_set(self, username, filename_list):
        #currently cannot test by swaggerui
        #print(username, filename_list, len(filename_list))
        clothes_data_ = self.collection.find({"username":username})
        if len(list(clothes_data_)) == 0:
            return False
        else:
            query = {
                "favorite_set": {
                    "$elemMatch": {
                        "clothes_list": {"$all": filename_list, "$size": len(filename_list)}
                    }
                },
                "username":username
            }
            # remove matched favrite_set by pull
            update = {
                "$pull": {
                    "favorite_set": {"clothes_list": {"$all": filename_list, "$size": len(filename_list)}}
                }
            }
            
            result = self.collection.update_many(query, update)
        return result.modified_count

    def __del__(self):
        self.client.close()
