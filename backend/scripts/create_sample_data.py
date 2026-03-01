import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime
from app.db.session import SessionLocal
from app.models.user import User
from app.models.project import Project
from app.models.interaction import Like, Comment, Favorite
from app.core.security import get_password_hash

def create_sample_data():
    db = SessionLocal()
    
    try:
        print("开始创建示例数据...")
        
        # 1. 创建示例用户
        print("创建示例用户...")
        sample_users = [
            {
                "username": "artist_01",
                "email": "artist01@example.com",
                "password": "password123",
                "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=artist01"
            },
            {
                "username": "designer_pro",
                "email": "designer@example.com",
                "password": "password123",
                "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=designer"
            },
            {
                "username": "3d_master",
                "email": "master@example.com",
                "password": "password123",
                "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=master"
            },
            {
                "username": "creative_mind",
                "email": "creative@example.com",
                "password": "password123",
                "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=creative"
            }
        ]
        
        created_users = []
        for user_data in sample_users:
            # 检查用户是否已存在
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                print(f"用户 {user_data['username']} 已存在，跳过创建")
                created_users.append(existing_user)
                continue
            
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                avatar_url=user_data["avatar_url"],
                is_active=True
            )
            db.add(user)
            db.flush()  # 获取用户ID
            created_users.append(user)
            print(f"创建用户: {user.username}")
        
        db.commit()
        
        # 2. 创建示例项目
        print("\n创建示例项目...")
        sample_projects = [
            {
                "name": "赛博朋克战士",
                "description": "一个充满未来科技感的赛博朋克风格战士角色，配备机械义肢和发光装甲。适合科幻游戏和动画项目。",
                "user_id": created_users[0].id,
                "thumbnail_url": "https://images.unsplash.com/photo-1614726365723-49cfae927846?w=800&h=600&fit=crop",
                "tags": ["赛博朋克", "科幻", "角色", "战士"],
                "view_count": 1250,
                "like_count": 89,
                "is_public": True,
                "status": "completed"
            },
            {
                "name": "魔法森林精灵",
                "description": "神秘的森林精灵角色，拥有自然魔法能力。精致的面部细节和华丽的服饰设计。",
                "user_id": created_users[1].id,
                "thumbnail_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800&h=600&fit=crop",
                "tags": ["奇幻", "精灵", "魔法", "自然"],
                "view_count": 980,
                "like_count": 76,
                "is_public": True,
                "status": "completed"
            },
            {
                "name": "机甲恐龙",
                "description": "将史前巨兽与未来科技完美结合的机甲恐龙。每一个细节都经过精心设计，展现力量与科技的融合。",
                "user_id": created_users[2].id,
                "thumbnail_url": "https://images.unsplash.com/photo-1569000972087-8d6eadea3e9d?w=800&h=600&fit=crop",
                "tags": ["机甲", "恐龙", "科幻", "机械"],
                "view_count": 2100,
                "like_count": 156,
                "is_public": True,
                "status": "completed"
            },
            {
                "name": "古风剑客",
                "description": "东方武侠风格的剑客角色，飘逸的长发和锋利的宝剑。适合古风游戏和影视项目。",
                "user_id": created_users[0].id,
                "thumbnail_url": "https://images.unsplash.com/photo-1615672963499-1148d2906e64?w=800&h=600&fit=crop",
                "tags": ["古风", "武侠", "剑客", "东方"],
                "view_count": 1680,
                "like_count": 112,
                "is_public": True,
                "status": "completed"
            },
            {
                "name": "蒸汽朋克探险家",
                "description": "维多利亚时代风格的蒸汽朋克探险家，配备各种奇妙的机械装置和探险装备。",
                "user_id": created_users[3].id,
                "thumbnail_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop",
                "tags": ["蒸汽朋克", "探险", "复古", "机械"],
                "view_count": 750,
                "like_count": 45,
                "is_public": True,
                "status": "completed"
            },
            {
                "name": "深海潜水员",
                "description": "现代深海探险潜水员角色，配备先进的潜水设备和照明系统。适合海洋探险类游戏。",
                "user_id": created_users[1].id,
                "thumbnail_url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&h=600&fit=crop",
                "tags": ["潜水", "海洋", "探险", "现代"],
                "view_count": 890,
                "like_count": 67,
                "is_public": True,
                "status": "completed"
            },
            {
                "name": "外星生物",
                "description": "来自遥远星球的神秘外星生物，独特的生理结构和奇异的外观设计。",
                "user_id": created_users[2].id,
                "thumbnail_url": "https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=800&h=600&fit=crop",
                "tags": ["外星", "科幻", "生物", "奇异"],
                "view_count": 1340,
                "like_count": 98,
                "is_public": True,
                "status": "completed"
            },
            {
                "name": "中世纪骑士",
                "description": "全副武装的中世纪骑士，闪亮的盔甲和威武的战马。展现骑士精神和荣耀。",
                "user_id": created_users[3].id,
                "thumbnail_url": "https://images.unsplash.com/photo-1598556851364-384f5c871c3d?w=800&h=600&fit=crop",
                "tags": ["中世纪", "骑士", "盔甲", "历史"],
                "view_count": 1560,
                "like_count": 134,
                "is_public": True,
                "status": "completed"
            }
        ]
        
        created_projects = []
        for project_data in sample_projects:
            # 检查项目是否已存在
            existing_project = db.query(Project).filter(Project.name == project_data["name"]).first()
            if existing_project:
                print(f"项目 '{project_data['name']}' 已存在，跳过创建")
                created_projects.append(existing_project)
                continue
            
            project = Project(
                name=project_data["name"],
                description=project_data["description"],
                user_id=project_data["user_id"],
                thumbnail_url=project_data["thumbnail_url"],
                tags=project_data["tags"],
                view_count=project_data["view_count"],
                like_count=project_data["like_count"],
                is_public=project_data["is_public"],
                status=project_data["status"]
            )
            db.add(project)
            db.flush()
            created_projects.append(project)
            print(f"创建项目: {project.name}")
        
        db.commit()
        
        # 3. 创建示例评论
        print("\n创建示例评论...")
        sample_comments = [
            {"project_id": created_projects[0].id, "user_id": created_users[1].id, "content": "太酷了！这个赛博朋克风格真的很到位，细节处理得很好。"},
            {"project_id": created_projects[0].id, "user_id": created_users[2].id, "content": "机械义肢的设计很有创意，发光效果也很棒！"},
            {"project_id": created_projects[1].id, "user_id": created_users[0].id, "content": "精灵的服饰设计太精美了，魔法效果也很自然。"},
            {"project_id": created_projects[2].id, "user_id": created_users[3].id, "content": "机甲和恐龙的结合简直是天才的想法，力量感十足！"},
            {"project_id": created_projects[3].id, "user_id": created_users[1].id, "content": "古风韵味十足，剑客的气质拿捏得很到位。"},
            {"project_id": created_projects[4].id, "user_id": created_users[2].id, "content": "蒸汽朋克的元素运用得很好，探险家的装备设计很有特色。"},
            {"project_id": created_projects[5].id, "user_id": created_users[0].id, "content": "深海氛围营造得很好，潜水装备的细节也很到位。"},
            {"project_id": created_projects[6].id, "user_id": created_users[3].id, "content": "外星生物的设计很有想象力，完全不同于地球上的生物。"},
            {"project_id": created_projects[7].id, "user_id": created_users[1].id, "content": "骑士的盔甲闪闪发光，很有中世纪的感觉！"},
        ]
        
        for comment_data in sample_comments:
            comment = Comment(
                project_id=comment_data["project_id"],
                user_id=comment_data["user_id"],
                content=comment_data["content"]
            )
            db.add(comment)
            print(f"添加评论到项目 ID {comment_data['project_id']}")
        
        db.commit()
        
        print("\n✅ 示例数据创建完成！")
        print(f"- 创建了 {len(created_users)} 个用户")
        print(f"- 创建了 {len(created_projects)} 个项目")
        print(f"- 添加了 {len(sample_comments)} 条评论")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 创建示例数据时出错: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
