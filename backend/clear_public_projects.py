from app.db.session import engine
from sqlalchemy import text

def clear_public_projects():
    try:
        with engine.connect() as conn:
            # 查询所有公开的项目
            result = conn.execute(text("SELECT id, name, user_id FROM projects WHERE is_public = 1"))
            public_projects = result.fetchall()
            
            if not public_projects:
                print("没有找到公开的项目")
                return
            
            print(f"找到 {len(public_projects)} 个公开项目:")
            for project in public_projects:
                print(f"  - ID: {project[0]}, 名称: {project[1]}, 用户ID: {project[2]}")
            
            # 删除所有公开的项目
            conn.execute(text("DELETE FROM projects WHERE is_public = 1"))
            conn.commit()
            
            print(f"\n成功删除 {len(public_projects)} 个公开项目")
        
    except Exception as e:
        print(f"删除公开项目时出错: {e}")

if __name__ == "__main__":
    clear_public_projects()