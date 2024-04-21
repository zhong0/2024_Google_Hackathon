import google.generativeai as genai

class GeminiService:
    def __init__(self, API_key, model_name):
        genai.configure(api_key=API_key)
        self.model = genai.GenerativeModel(model_name)

    def recommend_by_text(self, query) :
        chat = self.model.start_chat(history=[])
        return chat.send_message(query).text

    # def image_2_text(self, image, templateQuery)