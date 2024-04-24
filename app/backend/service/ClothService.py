from dao.ClothesDao import ClothesDao
import utils.Const as const

class ClothesService:
    def __init__(self):
        self.dao = ClothesDao(const.uri, const.username, const.password, const.db_name, const.clothes_collection)

    def get_category(self, username):
        return self.dao.get_all_distinct_category(username)

    def get_style(self, username):
        return self.dao.get_all_distinct_style(username)

    def get_occasion(self, username):
        return self.dao.get_all_distinct_occasion(username)
    
    def get_all_clothes_info(self, username):
        return self.dao.get_all_clothes_info(username)

    def get_file_path(self, username):
        return self.dao.get_all_distinct_filename(username)
    
    def get_file_path_group_by_category(self, username):
        category_files = {}

        categories = self.dao.get_all_distinct_category(username)

        for c in categories:
            filenames = self.dao.get_filename_by_category(username, c)
            
            if c in category_files:
                category_files[c].extend(filenames)  
            else:
                category_files[c] = filenames  

        return category_files

    def get_style_by_filename(self, username, filename):
        return self.dao.get_style_by_filename(username, filename)

    def insert_favorite_set(self, username, filename_list):
        return self.dao.insert_favorite_set(username, filename_list)