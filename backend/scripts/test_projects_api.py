import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 先登录获取token
login_data = {
    "email": "test@example.com",
    "password": "123456"
}

print("=" * 50)
print("测试项目API")
print("=" * 50)

# 1. 登录
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

# 2. 创建项目
print("\n2. 创建项目...")
project_data = {
    "name": "测试项目1",
    "description": "这是一个测试项目"
}
response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
if response.status_code == 201:
    project1 = response.json()
    print(f"✅ 项目创建成功: ID={project1['id']}, 名称={project1['name']}")
else:
    print(f"❌ 项目创建失败: {response.status_code}")
    print(response.text)

# 3. 再创建几个项目
print("\n3. 批量创建项目...")
for i in range(2, 5):
    response = requests.post(f"{BASE_URL}/projects/", json={
        "name": f"测试项目{i}",
        "description": f"这是测试项目{i}"
    }, headers=headers)
    if response.status_code == 201:
        print(f"✅ 项目{i}创建成功")
    else:
        print(f"❌ 项目{i}创建失败")

# 4. 获取项目列表
print("\n4. 获取项目列表...")
response = requests.get(f"{BASE_URL}/projects/", headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"✅ 获取项目列表成功")
    print(f"   总数: {data['total']}")
    print(f"   当前页: {data['page']}")
    print(f"   项目数量: {len(data['items'])}")
    for p in data['items'][:3]:
        print(f"   - {p['name']} (ID: {p['id']}, 状态: {p['status']})")
else:
    print(f"❌ 获取项目列表失败: {response.status_code}")

# 5. 获取项目详情
print("\n5. 获取项目详情...")
response = requests.get(f"{BASE_URL}/projects/{project1['id']}", headers=headers)
if response.status_code == 200:
    detail = response.json()
    print(f"✅ 获取项目详情成功")
    print(f"   名称: {detail['name']}")
    print(f"   描述: {detail['description']}")
    print(f"   状态: {detail['status']}")
    print(f"   创建时间: {detail['created_at']}")
else:
    print(f"❌ 获取项目详情失败: {response.status_code}")

# 6. 更新项目
print("\n6. 更新项目...")
update_data = {
    "name": "测试项目1（已更新）",
    "description": "这是更新后的描述"
}
response = requests.put(f"{BASE_URL}/projects/{project1['id']}", json=update_data, headers=headers)
if response.status_code == 200:
    updated = response.json()
    print(f"✅ 项目更新成功")
    print(f"   新名称: {updated['name']}")
    print(f"   新描述: {updated['description']}")
else:
    print(f"❌ 项目更新失败: {response.status_code}")

# 7. 更新项目状态
print("\n7. 更新项目状态...")
response = requests.put(f"{BASE_URL}/projects/{project1['id']}/status", 
                       json={"status": "processing"}, headers=headers)
if response.status_code == 200:
    print(f"✅ 项目状态更新成功: {response.json()['status']}")
else:
    print(f"❌ 项目状态更新失败: {response.status_code}")

# 8. 复制项目
print("\n8. 复制项目...")
response = requests.post(f"{BASE_URL}/projects/{project1['id']}/duplicate", headers=headers)
if response.status_code == 200:
    duplicated = response.json()
    print(f"✅ 项目复制成功: ID={duplicated['id']}, 名称={duplicated['name']}")
else:
    print(f"❌ 项目复制失败: {response.status_code}")

# 9. 搜索项目
print("\n9. 搜索项目...")
response = requests.get(f"{BASE_URL}/projects/?search=已更新", headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"✅ 搜索成功，找到 {len(data['items'])} 个项目")
else:
    print(f"❌ 搜索失败: {response.status_code}")

# 10. 筛选项目状态
print("\n10. 按状态筛选项目...")
response = requests.get(f"{BASE_URL}/projects/?status=processing", headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"✅ 筛选成功，找到 {len(data['items'])} 个processing状态的项目")
else:
    print(f"❌ 筛选失败: {response.status_code}")

# 11. 删除项目
print("\n11. 删除项目...")
response = requests.delete(f"{BASE_URL}/projects/{project1['id']}", headers=headers)
if response.status_code == 200:
    print(f"✅ 项目删除成功")
else:
    print(f"❌ 项目删除失败: {response.status_code}")

# 12. 再次获取列表确认删除
print("\n12. 确认删除后的项目列表...")
response = requests.get(f"{BASE_URL}/projects/", headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"✅ 当前项目总数: {data['total']}")

print("\n" + "=" * 50)
print("项目API测试完成！")
print("=" * 50)
