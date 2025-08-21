import pandas as pd
import re
import json
from thefuzz import process, fuzz

KEYWORD_SYNONYMS = {
    '치킨': ['후라이드', '프라이드', '오리지널'],
    '통닭': ['후라이드', '프라이드', '오리지널']
}

def parse_menu_string(menu_str):
    """문자열 형태의 메뉴 리스트를 실제 리스트로 변환합니다."""
    try:
        return json.loads(menu_str)
    except (json.JSONDecodeError, TypeError):
        return []

def get_order_details(query: str, df: pd.DataFrame):
    """
    사용자의 모호한 주문 쿼리를 분석하여 가장 유사한 가게, 메뉴, 수량을 추천합니다.
    """
    # 1. 수량 추출 및 기본값 설정
    quantity_match = re.search(r'(\d+)\s?(개|잔|인분|마리)', query)
    quantity = 1
    if quantity_match:
        quantity = int(quantity_match.group(1))
        query_text = query.replace(quantity_match.group(0), '').strip()
    else:
        query_text = re.sub(r'\d+', '', query).strip()

    if 'menu_list' not in df.columns:
        df['menu_list'] = df['menu'].apply(parse_menu_string)

    # 2. 상호명이 일부 일치하는 경우
    store_names = df['name'].tolist()
    best_store_match = process.extractOne(query_text, store_names, scorer=fuzz.partial_ratio)
    
    if best_store_match and best_store_match[1] > 75:
        matched_store_name = best_store_match[0]
        store_info = df[df['name'] == matched_store_name].iloc[0]
        
        # --- ✨ 여기가 핵심 수정 영역입니다 ---
        # 가게를 찾았더라도, 쿼리에 키워드가 있는지 먼저 확인
        for keyword, synonyms in KEYWORD_SYNONYMS.items():
            if keyword in query_text:
                # 키워드가 있다면, 해당 가게 메뉴에서 동의어를 먼저 찾아봄
                for menu_item in store_info['menu_list']:
                    if any(synonym in menu_item for synonym in synonyms):
                        # 동의어가 포함된 메뉴를 찾았으면 즉시 반환!
                        return {
                            "restaurant": matched_store_name,
                            "item": menu_item,
                            "quantity": quantity,
                            "reason": f"'{matched_store_name}'에서 '{keyword}'와(과) 관련된 메뉴를 찾았어요."
                        }
        
        # 위 키워드 로직에서 메뉴를 찾지 못했을 경우에만, 기존의 유사도 검색 수행
        best_menu_match_in_store = process.extractOne(query_text, store_info['menu_list'])
        if best_menu_match_in_store:
            return {
                "restaurant": matched_store_name,
                "item": best_menu_match_in_store[0],
                "quantity": quantity,
                "reason": f"'{matched_store_name}'에서 가장 유사한 메뉴를 찾았어요."
            }
        # --- 수정 영역 끝 ---

    # 3. 상호명 매칭이 안됐을 경우, 전체 메뉴 대상 키워드 검색
    for keyword, synonyms in KEYWORD_SYNONYMS.items():
        if keyword in query_text:
            for index, row in df.iterrows():
                for menu_item in row['menu_list']:
                    if any(synonym in menu_item for synonym in synonyms):
                        return {
                            "restaurant": row['name'],
                            "item": menu_item,
                            "quantity": quantity,
                            "reason": f"'{keyword}'와(과) 가장 관련 있는 메뉴를 찾았어요."
                        }

    # 4. 모든 로직이 실패했을 경우, 최후의 전체 메뉴 대상 유사도 검색
    all_menus = []
    for index, row in df.iterrows():
        for menu_item in row['menu_list']:
            all_menus.append({'store': row['name'], 'menu': menu_item})

    best_menu_match = process.extractOne(query_text, [item['menu'] for item in all_menus], scorer=fuzz.token_set_ratio)
    
    if best_menu_match and best_menu_match[1] > 70:
        matched_menu_name = best_menu_match[0]
        for item in all_menus:
            if item['menu'] == matched_menu_name:
                return {
                    "restaurant": item['store'],
                    "item": matched_menu_name,
                    "quantity": quantity,
                    "reason": f"'{matched_menu_name}' 메뉴를 판매하는 가게를 찾았어요."
                }
                
    return None