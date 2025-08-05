
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import re
from difflib import get_close_matches

app = FastAPI(
    title="동국대 음성 주문 추천 API",
    description="음성으로 인식한 주문 텍스트에서 메뉴/가게/카테고리를 추출하고, 우선순위 가게를 추천합니다.",
    version="1.0.0"
)

# ✅ CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 요청 데이터 모델
class VoiceInput(BaseModel):
    text: str

# ✅ 음식점 데이터 로드
with open("dongguk_stores_normalized.json", "r", encoding="utf-8") as f:
    stores = json.load(f)

menu_items = list(set(item for store in stores for item in store["menu"]))
store_names = list(set(store["name"] for store in stores))
categories = list(set(store["category"] for store in stores))

# ✅ 유틸 함수
def normalize(text):
    return re.sub(r"[^\w가-힣]", "", text).lower()

def correct_keyword(keyword, options, cutoff=0.7):
    matches = get_close_matches(keyword, options, n=1, cutoff=cutoff)
    return matches[0] if matches else keyword

# ✅ 사용자 입력 분류 함수
def classify_order(text: str) -> dict:
    norm_text = normalize(text)

    matched_store = next((name for name in store_names if normalize(name) in norm_text), None)
    matched_menu = next((menu for menu in menu_items if normalize(menu) in norm_text), None)
    matched_category = next((cat for cat in categories if normalize(cat) in norm_text), None)

    # 오타 자동 보정
    if matched_menu:
        matched_menu = correct_keyword(matched_menu, menu_items)
    if matched_store:
        matched_store = correct_keyword(matched_store, store_names)
    if matched_category:
        matched_category = correct_keyword(matched_category, categories)

    if matched_store and matched_menu:
        return {"type": "가게+메뉴", "store": matched_store, "menu": matched_menu}
    elif matched_store:
        return {"type": "가게", "store": matched_store}
    elif matched_menu:
        return {"type": "메뉴", "menu": matched_menu}
    elif matched_category:
        return {"type": "카테고리", "category": matched_category}
    else:
        return {"type": "미분류", "raw": text}

# ✅ 메인 API 엔드포인트
@app.post("/api/nlp", summary="음성 텍스트 분석", description="음성 인식된 문장에서 메뉴/가게/카테고리를 추출하고 관련 가게를 추천합니다.")
async def nlp_process(data: VoiceInput):
    try:
        parsed = classify_order(data.text)
        top_result = {}

        if parsed["type"] == "가게+메뉴":
            matched = [
                s for s in stores
                if parsed["store"] in s["name"] and any(parsed["menu"] in m for m in s["menu"])
            ]
            if matched:
                top_result = matched[0]

        elif parsed["type"] == "가게":
            matched = [s for s in stores if parsed["store"] in s["name"]]
            if matched:
                top_result = matched[0]

        elif parsed["type"] == "메뉴":
            matched = [s for s in stores if parsed["menu"] in s["menu"]]
            if matched:
                top_result = matched[0]

        elif parsed["type"] == "카테고리":
            matched = [s for s in stores if s["category"] == parsed["category"]]
            if matched:
                top_result = matched[0]

        return {
            "parsed": parsed,
            "result": top_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
