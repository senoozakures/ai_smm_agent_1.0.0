from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class PlatformType(str, Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    TELEGRAM = "telegram"
    LINKEDIN = "linkedin"


class ContentType(str, Enum):
    POST = "post"
    STORY = "story"
    REEL = "reel"
    VIDEO = "video"
    CAROUSEL = "carousel"


class ProductBase(BaseModel):
    name: str = Field(..., description="Название продукта/услуги")
    description: str = Field(..., description="Описание продукта")
    target_audience: str = Field(..., description="Целевая аудитория")
    platforms: List[PlatformType] = Field(..., description="Платформы для публикации")
    price: Optional[float] = Field(None, description="Цена продукта")
    category: Optional[str] = Field(None, description="Категория продукта")
    keywords: Optional[List[str]] = Field([], description="Ключевые слова")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    platforms: Optional[List[PlatformType]] = None
    price: Optional[float] = None
    category: Optional[str] = None
    keywords: Optional[List[str]] = None


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ContentPlan(BaseModel):
    product_id: int
    content_type: ContentType
    platforms: List[PlatformType]
    post_count: int = Field(default=5, ge=1, le=50)
    schedule: Optional[str] = Field(None, description="Расписание публикаций (cron format)")
    
    class Config:
        from_attributes = True
