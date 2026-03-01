from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.db.session import get_db
from app.models.project import Project
from app.models.user import User
from app.models.interaction import Comment, Favorite
from app.schemas.project import (
    GalleryProjectResponse,
    GalleryListResponse,
    GalleryProjectDetail,
    GalleryAuthorInfo,
)

router = APIRouter()


@router.get("/", response_model=GalleryListResponse)
async def list_gallery_projects(
    search: Optional[str] = Query(None, description="按名称搜索"),
    tag: Optional[str] = Query(None, description="按标签筛选"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(12, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    query = db.query(Project).filter(
        Project.is_public == True,
        Project.status == "completed"
    )
    
    if search:
        query = query.filter(Project.name.contains(search))
    
    if tag:
        query = query.filter(Project.tags.contains(f'"{tag}"'))
    
    allowed_sort_fields = ["created_at", "view_count", "like_count"]
    if sort_by not in allowed_sort_fields:
        sort_by = "created_at"
    
    if sort_order == "desc":
        query = query.order_by(getattr(Project, sort_by).desc())
    else:
        query = query.order_by(getattr(Project, sort_by).asc())
    
    total = query.count()
    projects = query.offset((page - 1) * page_size).limit(page_size).all()
    
    items = []
    for project in projects:
        author = db.query(User).filter(User.id == project.user_id).first()
        author_info = GalleryAuthorInfo(
            id=author.id,
            username=author.username,
            avatar_url=author.avatar_url
        ) if author else GalleryAuthorInfo(id=0, username="未知用户", avatar_url=None)
        
        # 统计评论数和收藏数
        comment_count = db.query(func.count(Comment.id)).filter(
            Comment.project_id == project.id
        ).scalar() or 0
        
        favorite_count = db.query(func.count(Favorite.id)).filter(
            Favorite.project_id == project.id
        ).scalar() or 0
        
        items.append(GalleryProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            thumbnail_url=project.thumbnail_url,
            author=author_info,
            view_count=project.view_count,
            like_count=project.like_count,
            comment_count=comment_count,
            favorite_count=favorite_count,
            tags=project.tags or [],
            created_at=project.created_at,
            status=project.status
        ))
    
    return GalleryListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{project_id}", response_model=GalleryProjectDetail)
async def get_gallery_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_public == True,
        Project.status == "completed"
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在或未公开"
        )
    
    project.view_count += 1
    db.commit()
    
    author = db.query(User).filter(User.id == project.user_id).first()
    author_info = GalleryAuthorInfo(
        id=author.id,
        username=author.username,
        avatar_url=author.avatar_url
    ) if author else GalleryAuthorInfo(id=0, username="未知用户", avatar_url=None)
    
    # 统计评论数和收藏数
    comment_count = db.query(func.count(Comment.id)).filter(
        Comment.project_id == project.id
    ).scalar() or 0
    
    favorite_count = db.query(func.count(Favorite.id)).filter(
        Favorite.project_id == project.id
    ).scalar() or 0
    
    return GalleryProjectDetail(
        id=project.id,
        name=project.name,
        description=project.description,
        thumbnail_url=project.thumbnail_url,
        author=author_info,
        view_count=project.view_count,
        like_count=project.like_count,
        comment_count=comment_count,
        favorite_count=favorite_count,
        tags=project.tags or [],
        model_data=project.model_data or {},
        created_at=project.created_at,
        updated_at=project.updated_at,
        status=project.status
    )


@router.get("/tags/list")
async def get_popular_tags(
    limit: int = Query(20, ge=1, le=100, description="返回标签数量"),
    db: Session = Depends(get_db)
):
    """获取热门标签列表"""
    projects = db.query(Project).filter(
        Project.is_public == True,
        Project.status == "completed"
    ).all()
    
    tag_counts = {}
    for project in projects:
        for tag in (project.tags or []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    sorted_tags = sorted(
        [{"name": tag, "count": count} for tag, count in tag_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:limit]
    
    return {"tags": sorted_tags}
