from app.db.session import engine
from sqlalchemy import text

def fix_foreign_keys():
    """修改外键约束，添加级联删除"""
    
    sql_commands = [
        # 删除旧的外键约束
        "ALTER TABLE content_reports DROP FOREIGN KEY content_reports_ibfk_2",
        "ALTER TABLE project_comments DROP FOREIGN KEY project_comments_ibfk_1",
        "ALTER TABLE project_downloads DROP FOREIGN KEY project_downloads_ibfk_1",
        "ALTER TABLE project_favorites DROP FOREIGN KEY project_favorites_ibfk_1",
        "ALTER TABLE project_likes DROP FOREIGN KEY project_likes_ibfk_1",
        
        # 添加新的外键约束（带级联删除）
        "ALTER TABLE content_reports ADD CONSTRAINT content_reports_ibfk_2 FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
        "ALTER TABLE project_comments ADD CONSTRAINT project_comments_ibfk_1 FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
        "ALTER TABLE project_downloads ADD CONSTRAINT project_downloads_ibfk_1 FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
        "ALTER TABLE project_favorites ADD CONSTRAINT project_favorites_ibfk_1 FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
        "ALTER TABLE project_likes ADD CONSTRAINT project_likes_ibfk_1 FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
    ]
    
    try:
        with engine.connect() as conn:
            for sql in sql_commands:
                try:
                    print(f"执行: {sql}")
                    conn.execute(text(sql))
                    conn.commit()
                    print("  ✓ 成功")
                except Exception as e:
                    print(f"  ✗ 失败: {e}")
                    # 继续执行下一个命令
        
        print("\n外键约束修改完成！")
        
    except Exception as e:
        print(f"修改外键约束时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_foreign_keys()