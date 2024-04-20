from dao.ClothesDao import ClothesDao
import utils.Const as const
import os

class ClothesService:
    def __init__(self):
        self.dao = ClothesDao(const.uri, const.username, const.password, const.db_name, const.collection_name)

    def get_category(self, username):
        return self.dao.get_all_distinct_category(username)

    def get_style(self, username):
        return self.dao.get_all_distinct_style(username)

    def get_scenario(self, username):
        return self.dao.get_all_distinct_scenario(username)

    def get_file_path(self, username):
        # 获取所有独特的文件名
        filename_list = self.dao.get_all_distinct_filename(username)
        # 构建完整的文件路径列表
        file_path_list = [os.path.join(const.path, username, filename) for filename in filename_list]
        return file_path_list
