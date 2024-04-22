from dao.ClothesDao import ClothesDao
from utils.GeminiService import GeminiService
import utils.Const as const

import os
import datetime
import asyncio
import PIL.Image
from bson.json_util import dumps

class UploadService:
    def __init__(self):
        self.cloth_dao = ClothesDao(const.uri, const.username, const.password, const.db_name, const.clothes_collection)

    async def upload_images(self, username, files):

        #path to save uploaded image
        path = os.path.join("..", "upload", username)
        if not os.path.exists(path):
            os.makedirs(path)

        #prepare input file and save image
        input_list = []
        file_name_list = []
        for f in files:
            input_list.append(PIL.Image.open(f.file))
            if os.path.exists(os.path.join(path, f.filename)):
                upload_time = datetime.datetime.utcnow().strftime('_%Y-%m-%d_%H-%M-%S')
                split_part = os.path.splitext(f.filename)
                f.filename = split_part[0] + upload_time + split_part[1]
            input_list[-1].save(os.path.join(path, f.filename))
            file_name_list.append(f.filename)
        
        #gemini generate content
        prompting = '''please describe images and fill in value column in following JSON format then return a list of JSON object.
        {
            "name":"",
            "uuid":"",
            "category":"",
            "gender":"",
            "warmth":"",
            "detail":{
            "color":"[]",
            "material":"[]",
            "pattern":"[]",
            "style":"[]",
            "modeling":"[]"
            "feature":"[]"
            },
            "description":"",
            "occasion":[],
            "filename":""
        }
        In warmth, please describe in levels from 1~10 in number.
        In gender, there are 3 possible value man, woman and unisex.
        In img_link, please provide related image or website url.
        Every words should be lowercase.
        '''
        #start generate contents by batch send too many images at a time could be 504
        gemini_service = GeminiService(const.API_key, const.model)
        img_responses = await gemini_service.img_2_text_in_batch_async(prompting, input_list, 6)

        #set file name
        for response_js,  filename in zip(img_responses, file_name_list):
            response_js["filename"] = os.path.join(username, filename)
        
        return self.cloth_dao.insert_clothes_2_username(username, img_responses)

    