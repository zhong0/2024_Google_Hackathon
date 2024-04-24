import google.generativeai as genai
import json

class GeminiService:
    def __init__(self, API_key, model_name):
        genai.configure(api_key=API_key)
        self.model = genai.GenerativeModel(model_name)

    def recommend_by_text(self, query) :
        chat = self.model.start_chat(history=[])
        return chat.send_message(query).text

    # def image_2_text(self, image, templateQuery)
    async def img_2_text_in_batch_async(self, prompting, input_list, batch_size=0):
        chat = self.model.start_chat(history=[])
        img_responses = []
        if batch_size == 0:
            batch_size = len(input_list)
        i=0
        while(i<len(input_list)):
            if i+batch_size > len(input_list):
                list_t = list(input_list[i:])
                list_t.append(prompting)
            else:
                list_t = list(input_list[i:i+batch_size])
                list_t.append(prompting)
            gemini_response = chat.send_message(list_t)
            gemini_response_js = json.loads(self.response_json_cleaning(gemini_response.text))
            img_responses.extend(gemini_response_js)
            i += batch_size
        return img_responses

    def response_json_cleaning(self, text):
        text = text[text.find('['):text.rfind(']')+1]
        return text