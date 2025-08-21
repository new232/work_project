from pprint import pprint
import openai

class Chatbot:
    def __init__(self, api_key):
        self.content = [{"role": "system", "content": "You are a helpful assistant"}]
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo-1106"
        self.last_response = None

    def add_user_message(self, message):
        self.content.append({"role": "user", "content": message})

    def send_request(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.content
        )
        self.last_response = response
        return response

    def add_response_message(self):
        if self.last_response:
            message = self.last_response.choices[0].message
            self.content.append({
                "role": message.role,
                "content": message.content
            })

    def get_last_response_content(self):
        if self.last_response:
            content = self.last_response.choices[0].message.content
            print(content)
            return content
        return None

# --- 실행 코드 ---

# API 키 설정 (실제 키로 교체 필요)
API_KEY = "sk-..." 

# 챗봇 인스턴스 생성
bot = Chatbot(api_key=API_KEY)

# 1차 사용자 메시지
user_input_1 = "Who won the world series in 2020?"
bot.add_user_message(user_input_1)
bot.send_request()
bot.add_response_message()
bot.get_last_response_content()

# 2차 사용자 메시지
user_input_2 = "Where was it played?"
bot.add_user_message(user_input_2)
bot.send_request()
bot.add_response_message()
bot.get_last_response_content()

# 최종 context 확인
pprint(bot.content)