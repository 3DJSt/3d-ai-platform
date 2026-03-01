import requests

try:
    response = requests.get('http://127.0.0.1:8000/')
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    print("API测试成功！")
except Exception as e:
    print(f"API测试失败: {e}")