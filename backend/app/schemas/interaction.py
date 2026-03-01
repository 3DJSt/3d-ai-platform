from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# 点赞相关
class LikeCreate(BaseModel):
    project_id: int

class LikeResponse(BaseModel):
    id: int
    user_id: int
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 评论相关
class CommentCreate(BaseModel):
    project_id: int
    content: str
    parent_id: Optional[int] = None

class CommentUpdate(BaseModel):
    content: str

class CommentAuthor(BaseModel):
    id: int
    username: str
    avatar_url: Optional[str] = None

class CommentResponse(BaseModel):
    id: int
    user_id: int
    project_id: int
    content: str
    parent_id: Optional[int]
    author: CommentAuthor
    created_at: datetime
    updated_at: Optional[datetime]
    replies: List['CommentResponse'] = []
    
    class Config:
        from_attributes = True

# 收藏相关
class FavoriteCreate(BaseModel):
    project_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 项目交互统计
class ProjectInteractionStats(BaseModel):
    project_id: int
    like_count: int
    comment_count: int
    favorite_count: int
    is_liked: bool = False
    is_favorited: bool = False

# 评论列表响应
class CommentListResponse(BaseModel):
    items: List[CommentResponse]
    total: int
    page: int
    page_size: int
