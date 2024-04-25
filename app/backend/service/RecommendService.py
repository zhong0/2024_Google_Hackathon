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
        history_recommend.append(recommend_result["recommend_result"]["recommend_set"])
        self.recommend_history_dao.create_history_recommend(username, history_recommend)

        # send result (recommend_set, discription)
        return recommend_result 
    
    def explore_outfit(self, username, style, recommend_count):
        # get user clothes from wardrobe
        user_clothes = self.clothes_dao.get_all_clothes_info(username)

        # if selected_style is empty ， get style list from user's wardrobe
        if style :
            style = self.clothes_dao.get_all_distinct_style(username)
 
        shop_clothes = self.shop_dao.get_all_shop_clothes_info()  

        # build query
        query = build_explore_query(user_clothes, shop_clothes, style, recommend_count)
        print("--------------------------")
        print("query: " , query)

        # send request to gemini
        response = self.gemini_service.recommend_by_text(query)
        print("--------------------------")
        print("response: " , response)

        # parse response to json formatt
        recommend_result = self.parse_response_to_json(str(response), recommend_count)

        # send result (recommend_set, discription, style)
        return recommend_result
    
    def explore_pieces_recommendation(self, username, style, specific_clothes_filename, recommend_count):
        user_specific_clothes = self.clothes_dao.get_clothes_info_by_filename(username, specific_clothes_filename)
        recommend_specific_clothes = self.shop_dao.get_clothes_info_by_filename(specific_clothes_filename)
        
        if style :
            style = self.clothes_dao.get_all_distinct_style(username)

        shop_clothes = self.shop_dao.get_all_shop_clothes_info()  
        user_clothes = self.clothes_dao.get_all_clothes_info(username)

        # build query
        query = build_explore_pieces_recommend(
            user_clothes, shop_clothes, style, user_specific_clothes, recommend_count)
        print("--------------------------")
        print("query: " , query)

        # send request to gemini
        response = self.gemini_service.recommend_by_text(query)
        print("--------------------------")
        print("response: " , response)

        # parse response to json formatt
        recommend_result = self.parse_response_to_json(str(response), recommend_count)

        # send result (recommend_set, discription, style)
        return recommend_result

    
    @staticmethod
    def parse_response_to_json(response, recommend_count):
        # 暫時寫死怎麼取其中json
        json_str = []
        if recommend_count == 1:
            json_str = response[7:-4]
        else:    
            json_str = response[7:-5]

        print("Extracted JSON string:", json_str)

        try:
            recommend_result = json.loads(json_str)
            return recommend_result
        except json.JSONDecodeError:
            print("Failed to decode JSON from response")
        
        return {}

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
