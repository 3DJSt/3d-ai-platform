import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("完整功能测试报告")
print("=" * 60)

# 测试结果记录
test_results = []

def run_test(test_name, test_func):
    """运行测试并记录结果"""
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print('='*60)
    try:
        result = test_func()
        test_results.append({
            "name": test_name,
            "status": "✅ 通过",
            "details": result
        })
        print(f"✅ {test_name} - 通过")
        return True
    except Exception as e:
        test_results.append({
            "name": test_name,
            "status": "❌ 失败",
            "error": str(e)
        })
        print(f"❌ {test_name} - 失败")
        print(f"错误: {e}")
        return False

# 1. 登录测试
def test_login():
    login_data = {
        "email": "test@example.com",
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return {"token": response.json()["access_token"]}
    else:
        raise Exception(f"登录失败: {response.status_code}, {response.text}")

# 2. 创建项目测试
def test_create_project():
    token = test_results[0]["details"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    project_data = {
        "name": "功能测试项目",
        "description": "这是一个功能测试项目"
    }
    response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"创建失败: {response.status_code}, {response.text}")

# 3. 获取项目列表测试
def test_get_projects():
    token = test_results[0]["details"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/projects/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"获取失败: {response.status_code}, {response.text}")

# 4. 更新项目测试
def test_update_project():
    token = test_results[0]["details"]["token"]
    project_id = test_results[1]["details"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "name": "功能测试项目（已更新）",
        "description": "更新后的描述"
    }
    response = requests.put(f"{BASE_URL}/projects/{project_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"更新失败: {response.status_code}, {response.text}")

# 5. 更新项目状态测试
def test_update_status():
    token = test_results[0]["details"]["token"]
    project_id = test_results[1]["details"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.put(f"{BASE_URL}/projects/{project_id}/status", 
                       json={"status": "completed"}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"状态更新失败: {response.status_code}, {response.text}")

# 6. 复制项目测试
def test_duplicate_project():
    token = test_results[0]["details"]["token"]
    project_id = test_results[1]["details"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/projects/{project_id}/duplicate", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"复制失败: {response.status_code}, {response.text}")

# 7. 发表项目测试
def test_publish_project():
    token = test_results[0]["details"]["token"]
    project_id = test_results[1]["details"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.put(f"{BASE_URL}/projects/{project_id}/publish", 
                       json={"is_public": True, "allow_download": True}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"发表失败: {response.status_code}, {response.text}")

# 8. 获取公共项目列表测试
def test_get_public_projects():
    response = requests.get(f"{BASE_URL}/projects/public/list")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"获取公共项目失败: {response.status_code}, {response.text}")

# 9. 点赞测试
def test_like_project():
    token = test_results[0]["details"]["token"]
    project_id = test_results[1]["details"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/projects/{project_id}/like", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"点赞失败: {response.status_code}, {response.text}")

# 10. 收藏测试
def test_favorite_project():
    token = test_results[0]["details"]["token"]
    project_id = test_results[1]["details"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/projects/{project_id}/favorite", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"收藏失败: {response.status_code}, {response.text}")

# 11. 添加评论测试
def test_add_comment():
    token = test_results[0]["details"]["token"]
    project_id = test_results[1]["details"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    comment_data = {"content": "这是一条测试评论"}
    response = requests.post(f"{BASE_URL}/projects/{project_id}/comments", 
                        json=comment_data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"添加评论失败: {response.status_code}, {response.text}")

# 12. 获取评论测试
def test_get_comments():
    token = test_results[0]["details"]["token"]
    project_id = test_results[1]["details"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/projects/{project_id}/comments", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"获取评论失败: {response.status_code}, {response.text}")

# 13. 删除项目测试
def test_delete_project():
    token = test_results[0]["details"]["token"]
    project_id = test_results[1]["details"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.delete(f"{BASE_URL}/projects/{project_id}", headers=headers)
    if response.status_code == 200:
        return {"message": "删除成功"}
    else:
        raise Exception(f"删除失败: {response.status_code}, {response.text}")

# 执行所有测试
run_test("1. 用户登录", test_login)
run_test("2. 创建项目", test_create_project)
run_test("3. 获取项目列表", test_get_projects)
run_test("4. 更新项目", test_update_project)
run_test("5. 更新项目状态", test_update_status)
run_test("6. 复制项目", test_duplicate_project)
run_test("7. 发表项目", test_publish_project)
run_test("8. 获取公共项目列表", test_get_public_projects)
run_test("9. 点赞项目", test_like_project)
run_test("10. 收藏项目", test_favorite_project)
run_test("11. 添加评论", test_add_comment)
run_test("12. 获取评论", test_get_comments)
run_test("13. 删除项目", test_delete_project)

# 生成测试报告
print("\n" + "=" * 60)
print("测试结果汇总")
print("=" * 60)

passed = sum(1 for t in test_results if t["status"] == "✅ 通过")
failed = sum(1 for t in test_results if t["status"] == "❌ 失败")

print(f"\n总测试数: {len(test_results)}")
print(f"通过: {passed}")
print(f"失败: {failed}")
print(f"通过率: {passed/len(test_results)*100:.1f}%")

print("\n详细结果:")
for i, result in enumerate(test_results, 1):
    print(f"{i}. {result['name']}: {result['status']}")
    if result['status'] == "❌ 失败":
        print(f"   错误: {result.get('error', 'Unknown')}")

print("\n" + "=" * 60)