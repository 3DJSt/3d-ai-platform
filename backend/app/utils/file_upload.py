from minio import Minio
from app.core.config import settings
from typing import Optional, Tuple
import uuid
import os

# 初始化MinIO客户端
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

def upload_file(bucket_name: str, file_path: str, content_type: str) -> Tuple[str, str]:
    """上传文件到MinIO"""
    # 生成唯一文件名
    file_ext = os.path.splitext(file_path)[1]
    file_name = f"{uuid.uuid4().hex}{file_ext}"
    
    # 上传文件
    minio_client.fput_object(
        bucket_name=bucket_name,
        object_name=file_name,
        file_path=file_path,
        content_type=content_type
    )
    
    # 返回文件地址和名称
    file_url = f"{settings.MINIO_ENDPOINT}/{bucket_name}/{file_name}"
    return file_url, file_name