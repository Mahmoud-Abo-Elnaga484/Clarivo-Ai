import os
import requests
from dotenv import load_dotenv

load_dotenv()

LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL")

def call_local_llm(prompt: str, max_new_tokens: int = 800, temperature: float = 0.3) -> str:
    if not LOCAL_LLM_URL:
        raise ValueError("LOCAL_LLM_URL مش موجود في .env!")

    endpoint = f"{LOCAL_LLM_URL.rstrip('/')}/generate"
    payload = {
        "prompt": prompt,
        "max_new_tokens": max_new_tokens,
        "temperature": temperature,
    }
    
    headers = {
        "ngrok-skip-browser-warning": "69420",
        "Content-Type": "application/json"
    }

    # السطور دي هتطبع في التيرمينال عندك عشان نتأكد إن الرابط سليم والطلب بيتبعت
    print(f"\n[Debug] 🚀 Sending request to Kaggle: {endpoint}")
    print(f"[Debug] 📦 Headers: {headers}")

    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=400)
        print(f"[Debug] 📥 Received status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except Exception as e:
        print(f"\n[Error] ❌ Failed to connect: {e}")
        raise ConnectionError(f"مش قادر يوصل لموديل Kaggle. تفاصيل الخطأ: {e}")