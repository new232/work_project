from fastapi import FastAPI, Query
from distance import geocode_address, calculate_distance
from supabase import get_all_stores, update_store_distance

app = FastAPI()

@app.get("/update-length")
def update_length_for_all_stores(address: str = Query(..., description="기준 지번 주소")):
    print(f"🔎 요청 주소: {address}")

    # 1. 입력 주소 → 좌표 변환
    try:
        user_lat, user_lon = geocode_address(address)
    except Exception as e:
        print(f"❌ 주소 변환 실패: {e}")
        return {"error": "주소 좌표 변환 실패"}

    # 2. Supabase에서 모든 가게 가져오기
    stores = get_all_stores()
    if not isinstance(stores, list):
        print(f"❌ 응답 형식 오류: {stores}")
        return {"error": "가게 목록 조회 실패"}

    updated_count = 0

    for store in stores:
        if not isinstance(store, dict):
            continue

        lat = store.get("latitude")
        lon = store.get("longitude")
        store_id = store.get("id")

        if lat is None or lon is None or store_id is None:
            continue

        try:
            dist = calculate_distance(user_lat, user_lon, lat, lon)
            update_store_distance(store_id, dist)
            updated_count += 1
        except Exception as e:
            print(f"❌ 거리 계산 실패(store_id={store_id}): {e}")
            continue

    return {"message": f"{updated_count}개 가게 거리 갱신 완료"}
