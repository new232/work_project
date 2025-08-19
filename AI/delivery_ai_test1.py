import json
import random
from typing import List, Dict, Any, Optional, Tuple

# --- 데이터베이스 시뮬레이션 ---
# 실제 환경에서는 DB 또는 외부 JSON 파일에서 이 데이터를 로드합니다.
RESTAURANT_DATA = {
    "restaurants": [
        {
            "id": 1,
            "name": "황금올리브 치킨",
            "category": "치킨",
            "address": "서울특별시 중구 필동로1길 30",
            "rating": 4.8,
            "menus": [
                {"name": "황금올리브치킨", "price": 20000},
                {"name": "자메이카 통다리구이", "price": 21500},
                {"name": "양념치킨", "price": 21500}
            ]
        },
        {
            "id": 2,
            "name": "BHC 치킨 동국대점",
            "category": "치킨",
            "address": "서울특별시 중구 서애로 10",
            "rating": 4.9,
            "menus": [
                {"name": "뿌링클", "price": 21000},
                {"name": "맛초킹", "price": 21000},
                {"name": "골드킹", "price": 21000}
            ]
        },
        {
            "id": 3,
            "name": "버거킹 충무로역점",
            "category": "버거",
            "address": "서울특별시 중구 퇴계로 212",
            "rating": 4.5,
            "menus": [
                {"name": "와퍼", "price": 7100},
                {"name": "콰트로치즈와퍼", "price": 7900},
                {"name": "통새우와퍼", "price": 7900}
            ]
        },
        {
            "id": 4,
            "name": "동국반점",
            "category": "중식",
            "address": "서울특별시 중구 필동로 22-5",
            "rating": 4.6,
            "menus": [
                {"name": "짜장면", "price": 6000},
                {"name": "짬뽕", "price": 8000},
                {"name": "탕수육", "price": 18000}
            ]
        }
    ]
}

class OrderAI:
    """
    음성 주문 AI의 핵심 로직을 처리하는 클래스입니다.
    사용자 입력 해석, 가게/메뉴 추천, 장바구니 관리, 주문 확정 등의 기능을 수행합니다.
    """
    def __init__(self):
        self.user_address: Optional[str] = None
        self.shopping_cart: List[Dict[str, Any]] = []
        self.state: str = "AWAITING_ADDRESS" # 현재 대화 상태를 관리합니다.

    def process_input(self, user_text: str) -> str:
        """사용자의 입력을 현재 상태에 따라 처리하고 적절한 응답을 반환합니다."""
        if self.state == "AWAITING_ADDRESS":
            # 주소 설정 단계
            self.user_address = user_text
            self.state = "AWAITING_ORDER"
            return f"배달 주소가 '{self.user_address}'(으)로 설정되었습니다. 무엇을 주문하시겠어요?"

        elif self.state == "AWAITING_ORDER":
            # 주문 접수 단계
            if not self.user_address:
                return "먼저 배달 받으실 주소를 말씀해주세요."

            # 1. 주변 가게 검색 (거리 기반 필터링)
            nearby_restaurants = self._find_nearby_restaurants(self.user_address)
            if not nearby_restaurants:
                return "죄송합니다. 3km 이내에 배달 가능한 가게가 없습니다."

            # 2. 사용자 의도 파악 (메뉴, 가게명 등 키워드 추출)
            # 실제 서비스에서는 자연어 처리(NLP) 모델을 사용하여 더 정교하게 분석합니다.
            keywords = self._extract_keywords(user_text)

            # 3. 최적의 가게와 메뉴 선정
            selected_item = self._select_best_option(keywords, nearby_restaurants)
            if not selected_item:
                return "죄송합니다. 주문하신 메뉴를 찾을 수 없거나, 해당 가게가 근처에 없습니다."

            # 4. 사용자에게 제안 및 확인
            self.temp_item = selected_item # 사용자가 확정하기 전 임시 저장
            self.state = "CONFIRMING_ITEM"
            restaurant = selected_item['restaurant']
            menu = selected_item['menu']
            return f"{restaurant['name']}의 {menu['name']} 메뉴를 주문하시겠습니까? 가격은 {menu['price']}원 입니다."

        elif self.state == "CONFIRMING_ITEM":
            # 주문 항목 확정 단계
            if any(word in user_text for word in ["응", "네", "좋아", "맞아", "주문해줘"]):
                self.shopping_cart.append(self.temp_item)
                self.temp_item = {}
                self.state = "AWAITING_MORE_ITEMS"
                total_price = sum(item['menu']['price'] for item in self.shopping_cart)
                return f"장바구니에 추가되었습니다. 현재 총 주문금액은 {total_price}원 입니다. 더 주문하시겠어요? 아니면 '주문 완료'라고 말씀해주세요."
            else:
                self.state = "AWAITING_ORDER"
                return "알겠습니다. 주문이 취소되었습니다. 다시 주문해주세요."

        elif self.state == "AWAITING_MORE_ITEMS":
            # 추가 주문 또는 주문 완료 단계
            if "주문 완료" in user_text:
                return self._finalize_order()
            else:
                self.state = "AWAITING_ORDER"
                return self.process_input(user_text) # 다시 주문 프로세스 시작

        return "죄송합니다. 잘 이해하지 못했습니다."

    def _find_nearby_restaurants(self, address: str) -> List[Dict[str, Any]]:
        """
        주어진 주소 근처(3km 이내)의 가게를 찾습니다.
        실제 서비스에서는 지도 API를 사용하여 정확한 거리를 계산해야 합니다.
        여기서는 시뮬레이션을 위해 랜덤 거리를 부여하고 필터링합니다.
        """
        all_restaurants = RESTAURANT_DATA['restaurants']
        nearby_list = []
        for r in all_restaurants:
            # 시뮬레이션을 위한 랜덤 거리 (0.1 ~ 5.0 km)
            distance = round(random.uniform(0.1, 5.0), 1)
            if distance <= 3.0:
                r_with_dist = r.copy()
                r_with_dist['distance'] = distance
                nearby_list.append(r_with_dist)
        return nearby_list

    def _extract_keywords(self, text: str) -> Dict[str, str]:
        """
        사용자 입력에서 가게명, 메뉴명 등의 키워드를 추출합니다.
        간단한 키워드 매칭 방식이며, 실제로는 형태소 분석 등 NLP 기술이 필요합니다.
        """
        keywords = {'menu': None, 'store': None}
        
        # 가게명 키워드 탐색
        for r in RESTAURANT_DATA['restaurants']:
            if r['name'] in text:
                keywords['store'] = r['name']
                break # 첫 번째로 발견된 가게명만 사용

        # 메뉴명 키워드 탐색 (가장 긴 단어 우선)
        # 예: "황금올리브치킨"과 "치킨"이 모두 포함된 경우 "황금올리브치킨"을 우선 인식
        found_menus = []
        for r in RESTAURANT_DATA['restaurants']:
            for m in r['menus']:
                if m['name'] in text:
                    found_menus.append(m['name'])
        
        if found_menus:
            keywords['menu'] = max(found_menus, key=len)
        elif '치킨' in text: keywords['menu'] = '치킨'
        elif '버거' in text or '햄버거' in text: keywords['menu'] = '버거'
        elif '짜장' in text: keywords['menu'] = '짜장면'

        return keywords

    def _select_best_option(self, keywords: Dict[str, str], restaurants: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        추출된 키워드와 주변 가게 목록을 바탕으로 최적의 가게와 메뉴를 선정합니다.
        선정 기준: 가게명 일치 > 메뉴명/카테고리 일치 > 평점 > 거리
        """
        candidates = restaurants

        # 1. 가게명으로 필터링
        if keywords['store']:
            candidates = [r for r in candidates if r['name'] == keywords['store']]
        
        if not candidates: return None

        # 2. 메뉴명/카테고리로 필터링 및 메뉴 선정
        best_match: Optional[Tuple[Dict, Dict, int]] = None # (가게, 메뉴, 점수)

        for r in candidates:
            for m in r['menus']:
                score = 0
                # 메뉴명이 정확히 일치하면 가장 높은 점수
                if keywords['menu'] and keywords['menu'] == m['name']:
                    score = 100
                # 메뉴 키워드가 메뉴명에 포함되면 중간 점수
                elif keywords['menu'] and keywords['menu'] in m['name']:
                    score = 50
                # 메뉴 키워드가 가게 카테고리와 일치하면 낮은 점수
                elif keywords['menu'] and keywords['menu'] == r['category']:
                    score = 10
                
                if score > 0:
                    if best_match is None or score > best_match[2]:
                        best_match = (r, m, score)

        if best_match:
            return {'restaurant': best_match[0], 'menu': best_match[1]}

        # 3. 메뉴 매칭 실패 시, 평점/거리 순으로 대표 메뉴 추천
        # 카테고리가 일치하는 가게 중 평점과 거리가 가장 좋은 곳의 첫 번째 메뉴를 추천
        if keywords['menu']:
            category_candidates = [r for r in candidates if r['category'] == keywords['menu']]
            if category_candidates:
                # 평점 내림차순, 거리 오름차순으로 정렬
                sorted_candidates = sorted(category_candidates, key=lambda x: (-x['rating'], x['distance']))
                best_restaurant = sorted_candidates[0]
                best_menu = best_restaurant['menus'][0]
                return {'restaurant': best_restaurant, 'menu': best_menu}

        return None

    def _finalize_order(self) -> str:
        """주문을 최종 확정하고 결과를 반환합니다."""
        if not self.shopping_cart:
            self.state = "AWAITING_ORDER"
            return "장바구니가 비어있습니다. 먼저 메뉴를 주문해주세요."

        total_price = sum(item['menu']['price'] for item in self.shopping_cart)
        order_summary = []
        for item in self.shopping_cart:
            summary = f"{item['restaurant']['name']} - {item['menu']['name']}"
            order_summary.append(summary)
        
        order_summary_text = ", ".join(order_summary)

        # 주문 정보 초기화
        self.shopping_cart = []
        self.state = "AWAITING_ORDER" # 다음 주문을 위해 상태 초기화

        # 가게에 주문 정보 전송 로직 (API 호출 등)
        print("\n[SYSTEM] 가게에 주문 정보를 전송합니다...")
        print(f"  - 주문자 주소: {self.user_address}")
        print(f"  - 주문 내역: {order_summary_text}")
        print(f"  - 결제 방식: 현장 결제")
        print("[SYSTEM] 주문 전송 완료.\n")

        return f"주문이 완료되었습니다. 주문 내역은 '{order_summary_text}' 이며, 총 결제 금액은 {total_price}원 입니다. 배달원에게 직접 결제해주세요."


# --- AI 서비스 시뮬레이션 실행 ---
def run_simulation():
    """대화형 시뮬레이션을 실행합니다."""
    ai = OrderAI()
    print("--- 음성 주문 AI 시뮬레이션을 시작합니다 ---")
    print("안녕하세요! 배달 서비스입니다. 먼저 배달 받으실 주소를 말씀해주세요.")
    
    while True:
        try:
            user_input = input("사용자: ")
            if user_input.lower() in ['exit', '종료']:
                print("AI: 이용해주셔서 감사합니다.")
                break
            
            ai_response = ai.process_input(user_input)
            print(f"AI: {ai_response}")

        except (KeyboardInterrupt, EOFError):
            print("\nAI: 시뮬레이션을 종료합니다.")
            break

if __name__ == "__main__":
    run_simulation()
