from sqlalchemy import Column, String, Text, JSON, Integer
from sqlalchemy.dialects.mysql import ENUM
from app.db.base import BaseModel

class Project(BaseModel):
    __tablename__ = "projects"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, index=True, nullable=False)  # 关联用户表id
    
    # 项目状态
    status = Column(ENUM("draft", "processing", "completed", "archived"), default="draft")
    # 项目数据
    model_data = Column(JSON, default={
        "model": None,
        "textures": [],
        "skeleton": None,
        "animations": [],
        "render_settings": {}
    })
    # 文件存储路径
    storage_paths = Column(JSON, default={
        "minio_bucket": "user-projects",
        "model_key": None,
        "texture_keys": [],
        "animation_keys": []
    })