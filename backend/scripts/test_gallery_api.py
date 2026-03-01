import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

login_data = {
    "email": "test@example.com",
    "password": "123456"
}

print("=" * 50)
print("测试画廊API")
print("=" * 50)

print("\n1. 用户登录...")
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✅ 登录成功，获取到token")
else:
    print(f"❌ 登录失败: {response.status_code}")
    print(response.text)
    exit(1)

print("\n2. 创建测试项目...")
project_data = {
    "name": "画廊测试项目1",
    "description": "这是一个用于测试画廊的项目"
}
response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
if response.status_code == 201:
    project1 = response.json()
    print(f"✅ 项目创建成功: ID={project1['id']}")
else:
    print(f"❌ 项目创建失败: {response.status_code}")
    print(response.text)
    project1 = None

if project1:
    print("\n3. 将项目状态更新为completed...")
    response = requests.put(f"{BASE_URL}/projects/{project1['id']}/status", 
                          json={"status": "completed"}, headers=headers)
    if response.status_code == 200:
        print(f"✅ 状态更新成功")
    else:
        print(f"❌ 状态更新失败: {response.status_code}")

    print("\n4. 将项目发布到画廊...")
    publish_data = {
        "is_public": True,
        "thumbnail_url": "https://example.com/thumb1.jpg",
        "tags": ["3D模型", "角色", "测试"]
    }
    response = requests.put(f"{BASE_URL}/projects/{project1['id']}/publish", 
                          json=publish_data, headers=headers)
    if response.status_code == 200:
        print(f"✅ 项目发布成功")
    else:
        print(f"❌ 项目发布失败: {response.status_code}")
        print(response.text)

print("\n5. 创建更多测试项目并发布...")
for i in range(2, 6):
    response = requests.post(f"{BASE_URL}/projects/", json={
        "name": f"画廊测试项目{i}",
        "description": f"这是测试项目{i}"
    }, headers=headers)
    
    if response.status_code == 201:
        proj = response.json()
        requests.put(f"{BASE_URL}/projects/{proj['id']}/status", 
                    json={"status": "completed"}, headers=headers)
        requests.put(f"{BASE_URL}/projects/{proj['id']}/publish", 
                    json={
                        "is_public": True,
                        "thumbnail_url": f"https://example.com/thumb{i}.jpg",
                        "tags": ["3D模型", f"类型{i}"]
                    }, headers=headers)
        print(f"✅ 项目{i}创建并发布成功")
    else:
        print(f"❌ 项目{i}创建失败")

print("\n6. 获取画廊项目列表（无需登录）...")
response = requests.get(f"{BASE_URL}/gallery/")
if response.status_code == 200:
    data = response.json()
    print(f"✅ 获取画廊列表成功")
    print(f"   总数: {data['total']}")
    print(f"   当前页: {data['page']}")
    print(f"   项目数量: {len(data['items'])}")
    for p in data['items'][:3]:
        print(f"   - {p['name']} (作者: {p['author']['username']}, 浏览: {p['view_count']}, 点赞: {p['like_count']})")
else:
    print(f"❌ 获取画廊列表失败: {response.status_code}")
    print(response.text)

print("\n7. 搜索画廊项目...")
response = requests.get(f"{BASE_URL}/gallery/?search=测试项目3")
if response.status_code == 200:
    data = response.json()
    print(f"✅ 搜索成功，找到 {len(data['items'])} 个项目")
else:
    print(f"❌ 搜索失败: {response.status_code}")

print("\n8. 按标签筛选...")
response = requests.get(f"{BASE_URL}/gallery/?tag=角色")
if response.status_code == 200:
    data = response.json()
    print(f"✅ 筛选成功，找到 {len(data['items'])} 个项目")
else:
    print(f"❌ 筛选失败: {response.status_code}")

print("\n9. 按浏览量排序...")
response = requests.get(f"{BASE_URL}/gallery/?sort_by=view_count&sort_order=desc")
if response.status_code == 200:
    data = response.json()
    print(f"✅ 排序成功")
else:
    print(f"❌ 排序失败: {response.status_code}")

print("\n10. 分页测试...")
response = requests.get(f"{BASE_URL}/gallery/?page=1&page_size=2")
if response.status_code == 200:
    data = response.json()
    print(f"✅ 分页成功")
    print(f"   当前页: {data['page']}")
    print(f"   每页数量: {data['page_size']}")
    print(f"   返回项目数: {len(data['items'])}")
else:
    print(f"❌ 分页失败: {response.status_code}")

if project1:
    print("\n11. 获取项目详情（会增加浏览量）...")
    response = requests.get(f"{BASE_URL}/gallery/{project1['id']}")
    if response.status_code == 200:
        detail = response.json()
        print(f"✅ 获取详情成功")
        print(f"   名称: {detail['name']}")
        print(f"   作者: {detail['author']['username']}")
        print(f"   浏览量: {detail['view_count']}")
        print(f"   标签: {detail['tags']}")
    else:
        print(f"❌ 获取详情失败: {response.status_code}")
        print(response.text)

    print("\n12. 再次获取详情确认浏览量增加...")
    response = requests.get(f"{BASE_URL}/gallery/{project1['id']}")
    if response.status_code == 200:
        detail = response.json()
        print(f"✅ 浏览量: {detail['view_count']} (应该比之前+1)")
    else:
        print(f"❌ 获取详情失败: {response.status_code}")

print("\n13. 获取热门标签...")
response = requests.get(f"{BASE_URL}/gallery/tags/list")
if response.status_code == 200:
    data = response.json()
    print(f"✅ 获取热门标签成功")
    print(f"   标签列表: {data['tags']}")
else:
    print(f"❌ 获取热门标签失败: {response.status_code}")

print("\n14. 测试未公开项目无法在画廊访问...")
if project1:
    response = requests.put(f"{BASE_URL}/projects/{project1['id']}/publish", 
                          json={"is_public": False}, headers=headers)
    response = requests.get(f"{BASE_URL}/gallery/{project1['id']}")
    if response.status_code == 404:
        print(f"✅ 正确：未公开项目无法访问")
    else:
        print(f"❌ 错误：未公开项目应该无法访问")

print("\n" + "=" * 50)
print("画廊API测试完成！")
print("=" * 50)
