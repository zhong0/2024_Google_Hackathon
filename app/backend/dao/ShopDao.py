from pymongo import MongoClient

class ShopDao:
    def __init__(self, uri, username, password, db_name, collection_name):
        self.client = MongoClient(uri, username=username, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    # def get_all_shop():
    #     return shop_list

    # def get_all_clothes_info_by_shop_list(shop_list):
    #     return clothes_list

    # def get_clothes_info_by_clothes_file_name(shop_name, cloth_name):
    #     return clothes_info