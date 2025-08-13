from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from app.models.product import PlatformType, ContentType


class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


class PostBase(BaseModel):
    title: Optional[str] = Field(None, description="Заголовок поста")
    text: str = Field(..., description="Текст поста")
    hashtags: List[str] = Field(default=[], description="Хештеги")
    platforms: List[PlatformType] = Field(..., description="Платформы для публикации")
    content_type: ContentType = Field(default=ContentType.POST, description="Тип контента")
    scheduled_time: Optional[datetime] = Field(None, description="Время публикации")
    image_prompt: Optional[str] = Field(None, description="Промпт для генерации изображения")
    video_script: Optional[str] = Field(None, description="Скрипт для видео")
    image_url: Optional[str] = Field(None, description="URL изображения для публикации")


class PostCreate(PostBase):
    product_id: int = Field(..., description="ID продукта")


class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    hashtags: Optional[List[str]] = None
    platforms: Optional[List[PlatformType]] = None
    content_type: Optional[ContentType] = None
    scheduled_time: Optional[datetime] = None
    image_prompt: Optional[str] = None
    video_script: Optional[str] = None


class Post(PostBase):
    id: int
    product_id: int
    status: PostStatus = PostStatus.DRAFT
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    analytics: Optional[Dict[str, Any]] = Field(default={}, description="Аналитика поста")
    
    class Config:
        from_attributes = True


class GeneratedContent(BaseModel):
    posts: List[PostCreate]
    images: List[str] = Field(default=[], description="URLs сгенерированных изображений")
    video_scripts: List[str] = Field(default=[], description="Скрипты для видео")
    hashtags: List[str] = Field(default=[], description="Популярные хештеги")


class ContentGenerationRequest(BaseModel):
    product_id: int
    content_type: ContentType = ContentType.POST
    post_count: int = Field(default=5, ge=1, le=20)
    platforms: List[PlatformType]
    tone: Optional[str] = Field("professional", description="Тон контента")
    include_images: bool = Field(default=True, description="Генерировать ли изображения")
    include_videos: bool = Field(default=False, description="Генерировать ли видео-скрипты")
