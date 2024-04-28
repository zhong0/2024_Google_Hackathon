from ..dao.ClothesDao import ClothesDao
from ..utils import Const as const
import os

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
    
    def get_favorite_set(self, username):
        return self.dao.get_favorite_set(username)

    def insert_favorite_set(self, username, filename_list, style, description):
        return self.dao.insert_favorite_set(username, filename_list, style, description)

    def remove_favorite_set(self, username, filename_list):
        return self.dao.remove_favorite_set(username, filename_list)

    def remove_clothes_from_wardrobe(self, username, filename):
        path = os.path.join("..", "upload", filename)
        print(str(path))
        try:
            os.remove(path)
            print("File deleted successfully.")
            return self.dao.remove_clothes_from_wardrobe(username, filename)
        except FileNotFoundError:
            print("Error: File not found.")
            return False
        except PermissionError:
            print("Error: Permission denied.")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False