from app.db.session import engine
from sqlalchemy import text, inspect

def check_foreign_keys():
    try:
        inspector = inspect(engine)
        
        print("检查 projects 表的外键约束:")
        print("=" * 60)
        
        # 获取所有引用 projects 表的外键
        for table_name in inspector.get_table_names():
            foreign_keys = inspector.get_foreign_keys(table_name)
            for fk in foreign_keys:
                if 'project' in str(fk.get('referred_table', '')):
                    print(f"\n表: {table_name}")
                    print(f"  外键名: {fk.get('name')}")
                    print(f"  列: {fk.get('constrained_columns')}")
                    print(f"  引用表: {fk.get('referred_table')}")
                    print(f"  引用列: {fk.get('referred_columns')}")
                    print(f"  ondelete: {fk.get('ondelete')}")
        
        print("\n" + "=" * 60)
        print("\n尝试直接查询外键约束:")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    TABLE_NAME,
                    COLUMN_NAME,
                    CONSTRAINT_NAME,
                    REFERENCED_TABLE_NAME,
                    REFERENCED_COLUMN_NAME
                FROM
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE
                    REFERENCED_TABLE_NAME = 'projects'
                    AND TABLE_SCHEMA = DATABASE()
            """))
            
            for row in result:
                print(f"\n表: {row[0]}")
                print(f"  列: {row[1]}")
                print(f"  约束名: {row[2]}")
                print(f"  引用表: {row[3]}")
                print(f"  引用列: {row[4]}")
                
    except Exception as e:
        print(f"检查外键时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_foreign_keys()