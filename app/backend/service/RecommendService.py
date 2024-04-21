from dao.RecommendHistoryDao import RecommendHistoryDao
from dao.ClothesDao import ClothesDao

from utils.QueryBuilder import build_recommend_query
from utils.GeminiService import GeminiService

import utils.Const as const
import json
    
class RecommendService:
    def __init__(self):
        self.recommend_history_dao = RecommendHistoryDao(const.uri, const.username, const.password, const.db_name, const.recommend_collection)
        self.clothes_dao = ClothesDao(const.uri, const.username, const.password, const.db_name, const.clothes_collection)
        self.gemini_service = GeminiService(const.API_key, const.model)
    
    def recommend_from_wardrobe(self, username, style, occasion, specific_clothes, isRefresh) :
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
        history_recommend.append(recommend_result['recommend_set'])
        self.recommend_history_dao.create_history_recommend(username, history_recommend)

        # send result (recommend_set, discription)
        return recommend_result 
    
    @staticmethod
    def parse_response_to_json(response):
        # get first '{' & last '}' position
        start = response.find("{", response.find("{") + 1) 
        end = response.rfind("}")  
        json_str = response[start:end]
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
