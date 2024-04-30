from ..dao.ShopDao import ShopDao
from ..dao.ClothesDao import ClothesDao
from ..utils import Const as const
import random

class ShopService:
    def __init__(self):
        self.shop_dao = ShopDao(const.uri, const.username, const.password, const.db_name, const.shop_collection)
        self.clothes_dao = ClothesDao(const.uri, const.username, const.password, const.db_name, const.clothes_collection)

    def get_all_shop_clothes_filename(self, username):
        return self.shop_dao.get_clothes_filename(username)
    
    def get_all_shop_clothes_info(self, username):
        return self.shop_dao.get_clothes_info(username)
    
    def get_shop_clothes_info_by_filename(self, username, filename):
        return self.shop_dao.get_clothes_info_by_filename(filename)
    
    def get_clothes_sale_info_by_filename(self, username, filename):
        return self.shop_dao.get_clothes_sale_info_by_filename(username, filename)
    
    def clothes_on_sale(self, username, filename, brand, size, price, owner_description):
        clothes_info = self.clothes_dao.get_clothes_info_by_filename(username, filename)
        sale_info = {
            "size": size,
            "brand": brand,
            "price": price,
            "owner_description": owner_description
        }

        if clothes_info:
            if clothes_info["filename"] == filename:
                clothes_info["sale_info"] = sale_info

        if clothes_info and self.clothes_dao.remove_clothes_from_wardrobe(username, filename):
            return self.shop_dao.clothes_on_sale(username, clothes_info)
        
        return False
    
    def remove_clothes_from_shop(self, username, filename):
        shop_clothes_info = self.shop_dao.get_clothes_info_by_filename(filename)
        if shop_clothes_info and self.clothes_dao.insert_clothes_2_username(username, [shop_clothes_info]):
            if self.shop_dao.remove_sale_clothes(username, filename):
                return True

        return False

    def update_sale_info(self, username, filename, brand, size, price, owner_description):
        clothes_info = self.shop_dao.get_clothes_info_by_filename(filename)
        sale_info = {
            "size": size,
            "brand": brand,
            "price": price,
            "owner_description": owner_description
        }

        if clothes_info:
            if clothes_info["filename"] == filename:
                clothes_info["sale_info"] = sale_info

        if clothes_info:
            return self.shop_dao.clothes_on_sale(username, clothes_info)
        
        return False


    def get_file_path_group_by_category(self, username):
        category_files = {}

        categories = self.shop_dao.get_all_distinct_category(username)

        for c in categories:
            filenames = self.shop_dao.get_filename_by_category(username, c)
            
            if c in category_files:
                category_files[c].extend(filenames)  
            else:
                category_files[c] = filenames  

        return category_files

    def get_all_user_filename(self):
        filename = self.shop_dao.get_all_user_filename()
        random.shuffle(filename)
        return filename[:25]