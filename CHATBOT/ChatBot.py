import os
import openai
import json
from pprint import pprint
import pandas as pd
import io
import recommend

class Chatbot:
    """
    배달대행 챗봇을 위한 프롬프트 엔지니어링 및 컨텍스트 관리 클래스
    """
    def __init__(self, csv_data, model_name="gpt-3.5-turbo", openai_api_key=None):
        if openai_api_key is None:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.model = model_name
        self.context = []

        # CSV 데이터를 DataFrame으로 로드하고 문자열로 변환하여 보관
        self.restaurant_data = pd.read_csv(io.StringIO(csv_data))
        self.restaurant_data_str = self.restaurant_data.to_string()

        self.set_system_role("당신은 배달대행 업무를 맡고 있는 친절한 AI 상담사입니다. 사용자의 주문 요청을 파악하고 정보를 추출하세요.")

    def set_system_role(self, role):
        """챗봇의 시스템 역할을 설정합니다."""
        self.context.append({"role": "system", "content": role})

    def get_order_instruction(self):
        """
        주문 요청에 필요한 구체적인 지시사항과 가게 목록을 반환합니다.
        """
        # AI에게 가게 목록 데이터를 함께 제공하여 정확한 정보 추출을 유도
        return (
            f"\n\nInstruction:\n"
            "아래 '가게 목록'을 참고해서 사용자 요청을 보고, 주문 정보를 **JSON** 형식으로 추출해줘. "
            "추출할 정보는 'restaurant'(음식점), 'items'(메뉴와 수량), 'address'(주소)야. "
            "사용자가 언급한 음식점 이름이 목록에 있다면, 목록에 있는 **정확한 주소**를 'address'에 넣어줘. "
            "만약 정보가 불충분하면 사용자에게 추가 정보를 요청하는 메시지를 보내줘. "
            "추출 후에는 사용자에게 배달이 곧 시작될 것이라는 친절한 메시지를 보내줘."
            "예시: {'restaurant': '삼겹싸롱 충무로점', 'items': [{'name': 'LA갈비', 'quantity': 1}], 'address': '서울 중구 충무로 29-1'}"
            "\n\n--- 가게 목록 ---\n"
            f"{self.restaurant_data_str}"
            "\n--- 가게 목록 끝 ---"
        )
    
    def process_order(self, user_input):
            """
            사용자의 주문 요청을 처리하고 AI 모델에 전달합니다.
            """
            full_prompt = user_input + self.get_order_instruction()
            
            self.context.append({"role": "user", "content": full_prompt})
            
            print("API에 전송될 전체 프롬프트:")
            print(user_input + "\n\nInstruction:\n[...가게 목록 데이터...]")
            print("-" * 50)
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.context,
                    temperature=0.2 # 정보 추출 작업이므로 온도를 낮춰 일관성을 높임
                )
                model_response = response.choices[0].message.content
                
                print("AI 모델 응답:")
                print(model_response)

                order_info = {}
                try:
                    # AI 응답에서 JSON 부분만 추출 시도
                    json_part = model_response[model_response.find('{'):model_response.rfind('}')+1]
                    order_info_str = json_part.replace("'", '"')
                    order_info = json.loads(order_info_str)
                except (json.JSONDecodeError, IndexError):
                    # JSON 추출 실패 시 빈 딕셔너리로 초기화
                    order_info = {}

                # recommend.py !
                if not order_info.get('restaurant'):
                    print("\n AI가 가게를 특정하지 못했습니다. 추천 시스템을 가동합니다...")
                    
                    # self.restaurant_data는 Chatbot 생성 시 로드된 pandas DataFrame
                    recommendation = recommend.get_order_details(user_input, self.restaurant_data)
                    
                    if recommendation:
                        # 추천 성공
                        rec_store = recommendation['restaurant']
                        rec_item = recommendation['item']
                        rec_qty = recommendation['quantity']
                        
                        final_response = (
                            f"혹시 '{rec_store}'의 '{rec_item}' {rec_qty}개 주문을 원하시나요? "
                            f"맞으시면 '응' 또는 '네'라고 답해주세요."
                        )
                        print(f"추천 결과: {recommendation}")
                    else:
                        # 추천실패. 이거 나오면 안되는뎅 ㅜ.ㅜ
                        final_response = "죄송하지만, 말씀하신 내용과 일치하는 가게나 메뉴를 찾지 못했어요. 조금 더 자세히 말씀해주시겠어요?"
                        print("추천 실패")

                    model_response = final_response
            
                self._clean_context()
                self.context.append({"role": "assistant", "content": model_response})
            
                return model_response
        
            except Exception as e:
                print(f"API 요청 중 오류 발생: {e}")
                self._clean_context()
                return "죄송합니다, 주문 처리 중 오류가 발생했습니다."


    def _clean_context(self):
        """
        컨텍스트에서 Instruction과 가게 목록을 제거합니다.
        """
        for message in reversed(self.context):
            if message["role"] == "user":
                cleaned_content = message["content"].split("\n\nInstruction:")[0].strip()
                message["content"] = cleaned_content
                break
    
    def get_context(self):
        """현재 컨텍스트를 반환합니다."""
        return self.context

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    file_path = os.path.join(parent_dir, 'backend', 'stores_rows.csv')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            csv_content = f.read()

        api_key_env = os.getenv("OPENAI_API_KEY")
    
        if api_key_env is None:
            print(" 환경 변수에 'OPENAI_API_KEY'가 설정되어 있지 않습니다.")
        else:
            chatbot = Chatbot(csv_data=csv_content, openai_api_key=api_key_env)
            
            user_input = "통닭"
            response = chatbot.process_order(user_input)
            
            print("\n=== 처리 결과 및 컨텍스트 확인 ===")
            print("최종 챗봇 응답:", response)
            print("\n정리된 컨텍스트:")
            pprint(chatbot.get_context())

    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다. 경로: {file_path}")
