import requests
from app.core.config import settings
from typing import Optional, Dict

def stable_diffusion_request(prompt: str) -> Optional[Dict]:
    """调用Stable Diffusion API生成图片"""
    if not settings.STABLE_DIFFUSION_API_KEY:
        raise ValueError("Stable Diffusion API Key未配置")
    
    url = f"{settings.STABLE_DIFFUSION_BASE_URL}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {settings.STABLE_DIFFUSION_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text_prompts": [{"text": prompt, "weight": 1}],
        "width": 1024,
        "height": 1024,
        "steps": 30
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # 抛出HTTP错误
    return response.json()