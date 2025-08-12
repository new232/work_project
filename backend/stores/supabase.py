import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

def get_all_stores():
    url = f"{SUPABASE_URL}/rest/v1/stores?select=id,latitude,longitude"
    response = requests.get(url, headers=headers)
    return response.json()

def update_store_distance(store_id: int, distance_km: float):
    url = f"{SUPABASE_URL}/rest/v1/stores?id=eq.{store_id}"
    payload = {
        "distance": distance_km
    }
    response = requests.patch(url, headers=headers, json=payload)
    return response.status_code
