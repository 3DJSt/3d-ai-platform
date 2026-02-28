import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.core.security import (
        get_password_hash,
        verify_password,
        create_access_token,
        decode_access_token
    )
    
    print("=== Security模块测试 ===")
    
    # 测试密码哈希（使用短密码避免bcrypt限制）
    password = "test123"
    hashed = get_password_hash(password)
    print(f"原始密码: {password}")
    print(f"哈希密码: {hashed}")
    
    # 测试密码验证
    is_valid = verify_password(password, hashed)
    print(f"密码验证: {'成功' if is_valid else '失败'}")
    
    # 测试错误密码验证
    is_invalid = verify_password("wrong", hashed)
    print(f"错误密码验证: {'失败' if not is_invalid else '成功'}")
    
    # 测试JWT令牌
    token_data = {"sub": "123", "role": "admin"}
    token = create_access_token(token_data)
    print(f"生成的令牌: {token[:50]}...")
    
    # 测试令牌解码
    decoded = decode_access_token(token)
    print(f"解码令牌: {decoded}")
    
    print("\n=== Security模块测试成功！===")
    
except Exception as e:
    print(f"Security模块测试失败: {e}")
    import traceback
    traceback.print_exc()