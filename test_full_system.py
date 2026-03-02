import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"
FRONTEND_URL = "http://localhost:5174"

def test_health_check():
    """测试后端健康检查"""
    print("\n" + "="*60)
    print("1. 测试后端健康检查")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ 后端服务正常: {response.json()}")
            return True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端服务连接失败: {e}")
        return False

def test_login():
    """测试用户登录"""
    print("\n" + "="*60)
    print("2. 测试用户登录")
    print("="*60)
    
    # 测试管理员登录
    login_data = {
        "email": "admin@3dai.com",
        "password": "admin123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 管理员登录成功")
            print(f"   用户名: {data['user']['username']}")
            print(f"   角色: {data['user']['role']}")
            return data['access_token']
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return None

def test_get_user_info(token):
    """测试获取用户信息"""
    print("\n" + "="*60)
    print("3. 测试获取用户信息")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=5)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ 获取用户信息成功")
            print(f"   ID: {user['id']}")
            print(f"   用户名: {user['username']}")
            print(f"   邮箱: {user['email']}")
            print(f"   角色: {user['role']}")
            return True
        else:
            print(f"❌ 获取用户信息失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取用户信息请求失败: {e}")
        return False

def test_projects_api(token):
    """测试项目API"""
    print("\n" + "="*60)
    print("4. 测试项目列表API")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/projects/", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取项目列表成功")
            print(f"   项目总数: {data.get('total', 0)}")
            print(f"   当前页: {data.get('page', 1)}")
            return True
        else:
            print(f"❌ 获取项目列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取项目列表请求失败: {e}")
        return False

def test_public_gallery():
    """测试公共画廊API"""
    print("\n" + "="*60)
    print("5. 测试公共画廊API")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/projects/public/list", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取公共画廊成功")
            print(f"   公开项目数: {data.get('total', 0)}")
            return True
        else:
            print(f"❌ 获取公共画廊失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取公共画廊请求失败: {e}")
        return False

def test_frontend():
    """测试前端页面"""
    print("\n" + "="*60)
    print("6. 测试前端页面访问")
    print("="*60)
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print(f"✅ 前端页面访问成功")
            print(f"   页面大小: {len(response.text)} 字节")
            return True
        else:
            print(f"❌ 前端页面访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端页面访问请求失败: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 3D AI 平台全系统测试")
    print("="*60)
    
    results = []
    
    # 1. 健康检查
    results.append(("后端健康检查", test_health_check()))
    
    # 2. 登录测试
    token = test_login()
    results.append(("用户登录", token is not None))
    
    if token:
        # 3. 获取用户信息
        results.append(("获取用户信息", test_get_user_info(token)))
        
        # 4. 项目API测试
        results.append(("项目列表API", test_projects_api(token)))
    else:
        print("\n⚠️  跳过需要登录的测试")
        results.append(("获取用户信息", False))
        results.append(("项目列表API", False))
    
    # 5. 公共画廊
    results.append(("公共画廊API", test_public_gallery()))
    
    # 6. 前端页面
    results.append(("前端页面访问", test_frontend()))
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"总计: {passed}/{total} 项测试通过")
    print("="*60)
    
    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常！")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 项测试失败，请检查相关服务")
        return 1

if __name__ == "__main__":
    sys.exit(main())
