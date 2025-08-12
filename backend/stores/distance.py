import requests
from math import radians, sin, cos, sqrt, atan2

def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "my-geocoder"}  # 중요: user-agent 없으면 차단됨
    res = requests.get(url, params={"q": address, "format": "json"}, headers=headers)

    try:
        data = res.json()
    except Exception as e:
        print("❌ JSON 파싱 에러:", e)
        print("📨 응답 내용:", res.text)
        raise e

    if not data:
        raise ValueError("❗ 주소에 대한 위치 정보를 찾을 수 없습니다.")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(R * c, 3)  # 소수점 3자리
