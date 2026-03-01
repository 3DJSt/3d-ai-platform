from app.db.session import engine
from sqlalchemy import text

def check_tables():
    """检查数据库中的表"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            print("数据库中的表:")
            print("=" * 60)
            for table in sorted(tables):
                print(f"  - {table}")
            
            print(f"\n总表数: {len(tables)}")
            
            # 检查需要的表是否存在
            required_tables = [
                'users', 'projects', 'likes', 'favorites', 
                'comments', 'content_reports', 'project_downloads'
            ]
            
            print("\n检查必需的表:")
            print("=" * 60)
            for table in required_tables:
                exists = table in tables
                status = "✅ 存在" if exists else "❌ 不存在"
                print(f"  {table}: {status}")
                
    except Exception as e:
        print(f"检查表时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_tables()