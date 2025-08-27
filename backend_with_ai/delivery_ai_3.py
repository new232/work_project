import json
import random
import os
import csv
from openai import OpenAI
from typing import List, Dict, Any, Optional, Tuple
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from uuid import uuid4

# --- 1. 데이터 처리 모듈 ---

def load_restaurant_data_from_local_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    로컬 CSV 파일에서 식당 데이터를 읽어와 파싱하고 그룹화합니다.
    안정적인 파일 경로를 위해 스크립트의 위치를 기준으로 경로를 계산합니다.
    """
    try:
        # 스크립트의 실제 위치를 기준으로 파일 경로를 구성합니다.
        script_dir = os.path.dirname(__file__)
        absolute_path = os.path.join(script_dir, file_path)
        
        with open(absolute_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            stores = {}
            for row in reader:
                store_name = row.get("매장명")
                if not store_name: continue

                if store_name not in stores:
                    stores[store_name] = {
                        "매장명": store_name,
                        "카테고리": row.get("카테고리"),
                        "주소": row.get("주소"),
                        "평점": row.get("평점") or 3.0,
                        "메뉴": []
                    }
                
                if row.get("메뉴명") and row.get("가격"):
                    try:
                        price = int(float(row["가격"]))
                        stores[store_name]["메뉴"].append({"메뉴명": row["메뉴명"], "가격": price})
                    except (ValueError, TypeError):
                        print(f"[Warning] '{store_name}'의 메뉴 '{row['메뉴명']}' 가격('{row['가격']}')이 유효하지 않아 제외합니다.")
                        continue
            return list(stores.values())
    except FileNotFoundError:
        print(f"[Error] CSV 파일을 찾을 수 없습니다: {absolute_path}")
        return []
    except Exception as e:
        print(f"[Error] CSV 데이터 처리 중 오류 발생: {e}")
        return []

# --- 2. AI 핵심 로직 클래스 ---

class OrderAI:
    """
    한 명의 사용자에 대한 주문 대화 세션을 관리하는 클래스입니다.
    """
    def __init__(self, restaurant_data: List[Dict[str, Any]]):
        self.restaurant_data = restaurant_data
        self.user_address: Optional[str] = None
        self.shopping_cart: List[Dict[str, Any]] = []
        self.state: str = "AWAITING_ADDRESS"
        self.temp_item: Optional[Dict[str, Any]] = None

        categories = set(r['카테고리'] for r in self.restaurant_data if r.get('카테고리'))
        self.available_categories = list(categories)
        
        self.client = None
        if os.environ.get("OPENAI_API_KEY"):
            self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        else:
            print("[Warning] OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

    def process_input(self, user_text: str) -> Dict[str, Any]:
        """사용자 입력을 처리하고 구조화된 응답을 반환합니다."""
        if self.state == "AWAITING_ADDRESS":
            self.user_address = user_text
            self.state = "AWAITING_ORDER"
            return {"status": "ADDRESS_SET", "message": f"배달 주소가 '{self.user_address}'(으)로 설정되었습니다. 무엇을 주문하시겠어요?"}

        elif self.state == "AWAITING_ORDER":
            nearby_restaurants = self._find_nearby_restaurants()
            if not nearby_restaurants:
                return {"status": "NO_RESTAURANTS", "message": "죄송합니다. 3km 이내에 배달 가능한 가게가 없습니다."}

            keywords = self._extract_keywords(user_text)
            selected_item = self._select_best_option(keywords, nearby_restaurants)
            if not selected_item:
                return {"status": "ITEM_NOT_FOUND", "message": "죄송합니다. 주문하신 메뉴를 찾을 수 없거나, 해당 가게가 근처에 없습니다."}

            self.temp_item = selected_item
            self.state = "CONFIRMING_ITEM"
            restaurant, menu = selected_item['restaurant'], selected_item['menu']
            return {
                "status": "ITEM_CONFIRMATION",
                "message": f"{restaurant['매장명']}의 {menu['메뉴명']} 메뉴를 주문하시겠습니까? 가격은 {menu['가격']}원 입니다.",
                "data": selected_item
            }

        elif self.state == "CONFIRMING_ITEM":
            if any(word in user_text for word in ["응", "네", "좋아", "맞아", "주문해줘"]):
                if self.temp_item: self.shopping_cart.append(self.temp_item)
                self.temp_item = None
                self.state = "AWAITING_MORE_ITEMS"
                total_price = sum(item['menu']['가격'] for item in self.shopping_cart)
                return {
                    "status": "ITEM_ADDED",
                    "message": f"장바구니에 추가되었습니다. 현재 총 주문금액은 {total_price}원 입니다. 더 주문하시겠어요? 아니면 '주문 완료'라고 말씀해주세요.",
                    "data": {"cart": self.shopping_cart, "total_price": total_price}
                }
            else:
                self.state = "AWAITING_ORDER"
                return {"status": "ITEM_REJECTED", "message": "알겠습니다. 주문이 취소되었습니다. 다시 주문해주세요."}

        elif self.state == "AWAITING_MORE_ITEMS":
            if "주문 완료" in user_text:
                return self._finalize_order()
            else:
                self.state = "AWAITING_ORDER"
                return self.process_input(user_text)

        return {"status": "ERROR", "message": "죄송합니다. 잘 이해하지 못했습니다."}

    def _find_nearby_restaurants(self) -> List[Dict[str, Any]]:
        # 시뮬레이션을 위해 매번 랜덤 거리를 계산합니다.
        nearby_list = []
        for r in self.restaurant_data:
            distance = round(random.uniform(0.1, 5.0), 1)
            if distance <= 3.0:
                r_with_dist = r.copy()
                r_with_dist['distance'] = distance
                r_with_dist['평점'] = r_with_dist.get('평점') or 3.0
                nearby_list.append(r_with_dist)
        return nearby_list


    def _extract_keywords(self, text: str) -> Dict[str, Optional[str]]:
        if not self.client: return self._simple_extract_keywords(text)
        try:
            prompt = f"""
            사용자 주문 텍스트에서 메뉴, 가게, 카테고리를 추출해줘.
            카테고리 목록: {self.available_categories}.
            결과는 JSON 형식으로 {{"menu": "메뉴명", "store": "가게이름", "category": "카테고리명"}}으로 반환하고, 없으면 null.
            입력: "{text}"
            출력:
            """
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content) if response.choices[0].message.content else {}
        except Exception as e:
            print(f"OpenAI API 오류: {e}. 기본 분석으로 전환.")
            return self._simple_extract_keywords(text)

    def _simple_extract_keywords(self, text: str) -> Dict[str, Optional[str]]:
        keywords: Dict[str, Optional[str]] = {'menu': None, 'store': None, 'category': None}
        for r in self.restaurant_data:
            if r['매장명'] in text:
                keywords.update({'store': r['매장명'], 'category': r.get('카테고리')}); break
        
        found_menus = [m['메뉴명'] for r in self.restaurant_data if '메뉴' in r and r['메뉴'] for m in r['메뉴'] if m['메뉴명'] in text]
        if found_menus: keywords['menu'] = max(found_menus, key=len)
        
        if not keywords['category']:
            for cat in self.available_categories:
                if cat in text: keywords['category'] = cat; break
        return keywords

    def _select_best_option(self, keywords: Dict[str, Optional[str]], restaurants: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        menu_kw, store_kw, cat_kw = keywords.get('menu'), keywords.get('store'), keywords.get('category')
        if menu_kw and not cat_kw and menu_kw in self.available_categories: cat_kw = menu_kw

        candidates = restaurants
        if store_kw: candidates = [r for r in candidates if r.get('매장명') == store_kw]
        elif cat_kw: candidates = [r for r in candidates if r.get('카테고리') == cat_kw]

        if menu_kw:
            best_match: Optional[Tuple[Dict, Dict, int]] = None
            for r in candidates:
                if '메뉴' in r and r['메뉴']:
                    for m in r['메뉴']:
                        score = 100 if menu_kw == m['메뉴명'] else 50 if menu_kw in m['메뉴명'] else 0
                        if score > 0 and (best_match is None or score > best_match[2]):
                            best_match = (r, m, score)
            if best_match: return {'restaurant': best_match[0], 'menu': best_match[1]}

        if candidates:
            sorted_candidates = sorted(candidates, key=lambda x: (-float(x.get('평점', 3.0)), x.get('distance', 99)))
            best_restaurant = sorted_candidates[0]
            if '메뉴' in best_restaurant and best_restaurant['메뉴']:
                return {'restaurant': best_restaurant, 'menu': best_restaurant['메뉴'][0]}
        return None

    def _finalize_order(self) -> Dict[str, Any]:
        if not self.shopping_cart:
            self.state = "AWAITING_ORDER"
            return {"status": "EMPTY_CART", "message": "장바구니가 비어있습니다. 먼저 메뉴를 주문해주세요."}

        total_price = sum(item['menu']['가격'] for item in self.shopping_cart)
        order_summary = ", ".join([f"{item['restaurant']['매장명']} - {item['menu']['메뉴명']}" for item in self.shopping_cart])
        
        final_order_data = {"cart": self.shopping_cart, "total_price": total_price, "summary": order_summary}
        
        print(f"\n[SYSTEM] 가게 주문 전송: 주소({self.user_address}), 내역({order_summary}), 결제(현장 결제)\n")

        # 세션 초기화
        self.shopping_cart = []
        self.state = "AWAITING_ORDER"
        
        return {
            "status": "ORDER_COMPLETE",
            "message": f"주문이 완료되었습니다. 주문 내역은 '{order_summary}' 이며, 총 결제 금액은 {total_price}원 입니다. 배달원에게 직접 결제해주세요.",
            "data": final_order_data
        }

# --- 3. Flask 웹 서버 설정 ---
app = Flask(__name__)
app.secret_key = os.urandom(24) # 세션 관리를 위한 시크릿 키
CORS(app)

# --- 전역 변수 및 초기화 ---
CSV_FILE_PATH = "stores_rows.csv"
RESTAURANT_DATA = load_restaurant_data_from_local_csv(CSV_FILE_PATH)
user_sessions: Dict[str, OrderAI] = {}

@app.before_request
def ensure_session():
    """모든 요청 전에 세션 ID를 확인하고, 없으면 생성합니다."""
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())

@app.route('/api/chat', methods=['POST'])
def chat():
    if not RESTAURANT_DATA:
        return jsonify({"status": "ERROR", "message": "AI 서비스가 식당 데이터 부족으로 초기화되지 않았습니다."}), 500

    session_id = session['session_id']
    # 해당 세션의 AI 인스턴스가 없으면 새로 생성
    if session_id not in user_sessions:
        user_sessions[session_id] = OrderAI(RESTAURANT_DATA)
    
    ai_instance = user_sessions[session_id]
    
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({"status": "ERROR", "message": "메시지가 없습니다."}), 400

    ai_response = ai_instance.process_input(user_message)
    return jsonify(ai_response)

# --- 4. 독립 실행 테스트용 함수 ---
def run_simulation():
    if not RESTAURANT_DATA:
        print("식당 데이터를 불러오지 못해 시뮬레이션을 시작할 수 없습니다.")
        return

    sim_ai = OrderAI(RESTAURANT_DATA)
    print("--- 음성 주문 AI 시뮬레이션을 시작합니다 ---")
    print("안녕하세요! 배달 서비스입니다. 먼저 배달 받으실 주소를 말씀해주세요.")
    
    while True:
        try:
            user_input = input("사용자: ")
            if user_input.lower() in ['exit', '종료']:
                print("AI: 이용해주셔서 감사합니다."); break
            
            ai_response = sim_ai.process_input(user_input)
            print(f"AI: {ai_response.get('message')}")
        except (KeyboardInterrupt, EOFError):
            print("\nAI: 시뮬레이션을 종료합니다."); break

if __name__ == '__main__':
    # Flask API 서버를 시작하려면 아래 라인의 주석을 해제하세요.
    app.run(debug=True, port=5000)
    
    # 독립적인 터미널 테스트를 원하시면 위 app.run()을 주석 처리하고 아래 라인의 주석을 해제하세요.
    # run_simulation()
