from sqlalchemy import Column, String, Text, JSON, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import BaseModel

class Project(BaseModel):
    __tablename__ = "projects"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, index=True, nullable=False)  # 关联用户表id
    
    # 项目状态
    status = Column(ENUM("draft", "processing", "completed", "archived"), default="draft")
    is_public = Column(Boolean, default=True, nullable=False)  # 是否公开
    allow_download = Column(Boolean, default=True, nullable=False)  # 是否允许下载
    
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

    # 关联关系
    reports = relationship("ContentReport", back_populates="project", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="project", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="project", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="project", cascade="all, delete-orphan")


class Like(BaseModel):
    __tablename__ = "project_likes"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联关系
    project = relationship("Project", back_populates="likes")
    user = relationship("User", back_populates="likes")


class Favorite(BaseModel):
    __tablename__ = "project_favorites"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联关系
    project = relationship("Project", back_populates="favorites")
    user = relationship("User", back_populates="favorites")


class Comment(BaseModel):
    __tablename__ = "project_comments"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联关系
    project = relationship("Project", back_populates="comments")
    user = relationship("User", back_populates="comments")
