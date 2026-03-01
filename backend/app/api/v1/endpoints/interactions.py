from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.interaction import Like, Comment, Favorite
from app.schemas.interaction import (
    LikeCreate, LikeResponse,
    CommentCreate, CommentUpdate, CommentResponse, CommentListResponse,
    FavoriteCreate, FavoriteResponse,
    ProjectInteractionStats, CommentAuthor
)

router = APIRouter()

# ==================== 点赞功能 ====================

@router.post("/like", response_model=LikeResponse)
async def like_project(
    like_data: LikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """点赞项目"""
    # 检查项目是否存在
    project = db.query(Project).filter(Project.id == like_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 检查是否已经点赞
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.project_id == like_data.project_id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="已经点赞过该项目")
    
    # 创建点赞
    like = Like(user_id=current_user.id, project_id=like_data.project_id)
    db.add(like)
    
    # 更新项目点赞数
    project.like_count += 1
    
    db.commit()
    db.refresh(like)
    return like

@router.delete("/like/{project_id}")
async def unlike_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """取消点赞"""
    like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.project_id == project_id
    ).first()
    
    if not like:
        raise HTTPException(status_code=404, detail="未找到点赞记录")
    
    # 删除点赞
    db.delete(like)
    
    # 更新项目点赞数
    project = db.query(Project).filter(Project.id == project_id).first()
    if project and project.like_count > 0:
        project.like_count -= 1
    
    db.commit()
    return {"message": "取消点赞成功"}

# ==================== 评论功能 ====================

@router.post("/comment", response_model=CommentResponse)
async def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建评论"""
    # 检查项目是否存在
    project = db.query(Project).filter(Project.id == comment_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 检查父评论是否存在（如果是回复）
    if comment_data.parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == comment_data.parent_id).first()
        if not parent_comment:
            raise HTTPException(status_code=404, detail="父评论不存在")
    
    # 创建评论
    comment = Comment(
        user_id=current_user.id,
        project_id=comment_data.project_id,
        content=comment_data.content,
        parent_id=comment_data.parent_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    # 构建响应
    return CommentResponse(
        id=comment.id,
        user_id=comment.user_id,
        project_id=comment.project_id,
        content=comment.content,
        parent_id=comment.parent_id,
        author=CommentAuthor(
            id=current_user.id,
            username=current_user.username,
            avatar_url=getattr(current_user, 'avatar_url', None)
        ),
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        replies=[]
    )

@router.get("/comments/{project_id}", response_model=CommentListResponse)
async def get_project_comments(
    project_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """获取项目评论列表"""
    # 只获取顶级评论（非回复）
    query = db.query(Comment).filter(
        Comment.project_id == project_id,
        Comment.parent_id == None
    ).order_by(Comment.created_at.desc())
    
    total = query.count()
    comments = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 构建响应
    items = []
    for comment in comments:
        author = db.query(User).filter(User.id == comment.user_id).first()
        
        # 获取回复
        replies_query = db.query(Comment).filter(Comment.parent_id == comment.id).order_by(Comment.created_at.asc())
        replies = replies_query.all()
        replies_response = []
        for reply in replies:
            reply_author = db.query(User).filter(User.id == reply.user_id).first()
            replies_response.append(CommentResponse(
                id=reply.id,
                user_id=reply.user_id,
                project_id=reply.project_id,
                content=reply.content,
                parent_id=reply.parent_id,
                author=CommentAuthor(
                    id=reply_author.id,
                    username=reply_author.username,
                    avatar_url=getattr(reply_author, 'avatar_url', None)
                ),
                created_at=reply.created_at,
                updated_at=reply.updated_at,
                replies=[]
            ))
        
        items.append(CommentResponse(
            id=comment.id,
            user_id=comment.user_id,
            project_id=comment.project_id,
            content=comment.content,
            parent_id=comment.parent_id,
            author=CommentAuthor(
                id=author.id,
                username=author.username,
                avatar_url=getattr(author, 'avatar_url', None)
            ),
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            replies=replies_response
        ))
    
    return CommentListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )

@router.delete("/comment/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    
    # 检查权限（只能删除自己的评论）
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限删除该评论")
    
    db.delete(comment)
    db.commit()
    return {"message": "删除成功"}

# ==================== 收藏功能 ====================

@router.post("/favorite", response_model=FavoriteResponse)
async def favorite_project(
    favorite_data: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """收藏项目"""
    # 检查项目是否存在
    project = db.query(Project).filter(Project.id == favorite_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 检查是否已经收藏
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.project_id == favorite_data.project_id
    ).first()
    
    if existing_favorite:
        raise HTTPException(status_code=400, detail="已经收藏过该项目")
    
    # 创建收藏
    favorite = Favorite(user_id=current_user.id, project_id=favorite_data.project_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

@router.delete("/favorite/{project_id}")
async def unfavorite_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """取消收藏"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.project_id == project_id
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="未找到收藏记录")
    
    db.delete(favorite)
    db.commit()
    return {"message": "取消收藏成功"}

@router.get("/favorites", response_model=list[FavoriteResponse])
async def get_user_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户收藏列表"""
    favorites = db.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    return favorites

# ==================== 交互统计 ====================

@router.get("/stats/{project_id}", response_model=ProjectInteractionStats)
async def get_project_interaction_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """获取项目交互统计"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 获取点赞数、评论数、收藏数
    like_count = db.query(func.count(Like.id)).filter(Like.project_id == project_id).scalar()
    comment_count = db.query(func.count(Comment.id)).filter(Comment.project_id == project_id).scalar()
    favorite_count = db.query(func.count(Favorite.id)).filter(Favorite.project_id == project_id).scalar()
    
    # 检查当前用户是否点赞/收藏
    is_liked = False
    is_favorited = False
    
    if current_user:
        is_liked = db.query(Like).filter(
            Like.user_id == current_user.id,
            Like.project_id == project_id
        ).first() is not None
        
        is_favorited = db.query(Favorite).filter(
            Favorite.user_id == current_user.id,
            Favorite.project_id == project_id
        ).first() is not None
    
    return ProjectInteractionStats(
        project_id=project_id,
        like_count=like_count,
        comment_count=comment_count,
        favorite_count=favorite_count,
        is_liked=is_liked,
        is_favorited=is_favorited
    )
