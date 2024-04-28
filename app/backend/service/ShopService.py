from ..dao.ShopDao import ShopDao
from ..utils import Const as const

class ShopService:
    def __init__(self):
         self.shop_dao = ShopDao(const.uri, const.username, const.password, const.db_name, const.shop_collection)

    def get_all_shop_clothes_filename(self, username):
        return self.shop_dao.get_clothes_filename(username)
    
    def get_all_shop_clothes_info(self, username):
        return self.shop_dao.get_clothes_info(username)
    
    def get_shop_clothes_info_by_filename(self, username, filename):
        return self.shop_dao.get_clothes_info_by_filename(filename)