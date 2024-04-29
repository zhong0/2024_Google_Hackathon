from dao.RecommendHistoryDao import RecommendHistoryDao
from dao.ClothesDao import ClothesDao
from dao.ShopDao import ShopDao

from utils.QueryBuilder import build_recommend_query, build_explore_query, build_explore_pieces_recommend
from utils.GeminiService import GeminiService

import utils.Const as const
import json
    
class RecommendService:
    def __init__(self):
        self.recommend_history_dao = RecommendHistoryDao(
            const.uri, const.username, const.password, const.db_name, const.recommend_collection)
        
        self.clothes_dao = ClothesDao(const.uri, const.username, const.password, 
                                      const.db_name, const.clothes_collection)
        
        self.shop_dao = ShopDao(const.uri, const.username, const.password, 
                                const.db_name, const.shop_collection)
        
        self.gemini_service = GeminiService(const.API_key, const.model)
    
    def recommend_from_wardrobe(self, username, style, occasion, specific_clothes, isRefresh):
        # get all clothes
        clothes = self.clothes_dao.get_all_clothes_info(username)   

        # if isRefresh is true : need to get history to avoid duplicate recommend
        history_recommend = []
        if isRefresh :
            history_recommend = self.recommend_history_dao.get_all_history_recommend(username)

        # build query
        query = build_recommend_query(clothes, style, occasion, specific_clothes, history_recommend)
        print("--------------------------")
        print("query: " , query)

        # send request to gemini
        response = self.gemini_service.recommend_by_text(query)
       
        # parse response to json formatt
        recommend_result = self.parse_response_to_json(response)
        print("--------------------------")
        print("result: ", recommend_result)

        # update history recommend
        recommend_set = recommend_result["recommend_result"]["recommend_set"]
        history_recommend.append(recommend_set)
        self.recommend_history_dao.create_history_recommend(username, history_recommend)

        favorite_set_list = self.clothes_dao.get_favorite_set(username)

        # recommend set is favorite set or not
        recommend_result["recommend_result"]["is_favorite_set"] = self.is_favorite_set(favorite_set_list, recommend_set)

        # send result (recommend_set, discription)
        return recommend_result
    
    def explore_outfit(self, username, style, recommend_count):
        # get user clothes from wardrobe
        user_clothes = self.clothes_dao.get_all_clothes_info(username)

        # if selected_style is empty ， get style list from user's wardrobe
        if not style :
            style = self.clothes_dao.get_all_distinct_style(username)
 
        shop_clothes = self.shop_dao.get_all_shop_clothes_info(username)  

        # build query
        query = build_explore_query(user_clothes, shop_clothes, style, recommend_count)
        print("--------------------------")
        print("query: " , query)

        # send request to gemini
        response = self.gemini_service.recommend_by_text(query)
        print("--------------------------")
        print("response: " , str(response))

        # parse response to json formatt
        recommend_result = self.parse_response_to_json(response)

        # send result (recommend_set, discription, style)
        return recommend_result
    
    def explore_pieces_recommendation(self, username, style, specific_clothes_filenames, recommend_count):
        specific_clothes = []
        for filename in specific_clothes_filenames:
            clothes_info = self.clothes_dao.get_clothes_info_by_filename(username, filename)
            if clothes_info:
                specific_clothes.append(clothes_info)
            
            clothes_info = self.shop_dao.get_clothes_info_by_filename(filename)
            if clothes_info:
                specific_clothes.append(clothes_info)    

        if not style :
            style = self.clothes_dao.get_all_distinct_style(username)

        shop_clothes = self.shop_dao.get_all_shop_clothes_info(username)  
        user_clothes = self.clothes_dao.get_all_clothes_info(username)

        # build query
        query = build_explore_pieces_recommend(
            user_clothes, shop_clothes, style, specific_clothes, recommend_count)
        print("--------------------------")
        print("query: " , query)

        # send request to gemini
        response = self.gemini_service.recommend_by_text(query)
        print("--------------------------")
        print("response: " , str(response))

        # parse response to json formatt
        recommend_result = self.parse_response_to_json(response)

        # send result (recommend_set, discription, style)
        return recommend_result

    @staticmethod
    def parse_response_to_json(response):

        lines = response.split('\n')
        json_line = ""
        for line in lines :
            print("---------------")
            print(line)
            if line and line[0] != '`':
                json_line = json_line + line
        
        json_str = json_line
        print("Extracted JSON string:", json_str)

        try:
            recommend_result = json.loads(json_str)
            return recommend_result
        except json.JSONDecodeError:
            print("Failed to decode JSON from response")
        
        return {}
    
    @staticmethod
    def is_favorite_set(favorite_set_list, recommend_set):
        for favorite_set in favorite_set_list:
            if sorted(favorite_set["clothes_list"]) == sorted(recommend_set):
                return True
        return False

    # for test
    def create_history_recommend(self, username, recommend_set):
        return self.dao.create_history_recommend(username, recommend_set)
    
    # for test
    def get_all_history_recommend(self, username):
        return self.dao.get_all_history_recommend(username)

    # for test
    def insert_history_recommend(self, username, recommend_set):
        return self.dao.insert_history_recommend(username, recommend_set)

    # for test
    def remove_history_recommend(self, username):
        return self.dao.remove_history_recommend(username)
