from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.content import ContentGenerationRequest, GeneratedContent, PostCreate
from app.models.product import Product
from app.services.content.generator import ContentGenerator
from app.models.product import PlatformType

router = APIRouter()


@router.post("/generate", response_model=GeneratedContent)
async def generate_content(
    request: ContentGenerationRequest,
    db: Session = Depends(get_db)
):
    """Генерация контента для продукта"""
    
    # Здесь должна быть логика получения продукта из БД
    # Пока что создаем заглушку
    product = Product(
        id=request.product_id,
        name="Тестовый продукт",
        description="Описание тестового продукта",
        target_audience="Целевая аудитория",
        platforms=request.platforms,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    generator = ContentGenerator()
    content = await generator.generate_content(product, request)
    
    return content


@router.post("/generate/posts", response_model=List[PostCreate])
async def generate_posts(
    product_id: int,
    count: int = 5,
    tone: str = "professional",
    db: Session = Depends(get_db)
):
    """Генерация только постов"""
    
    # Здесь должна быть логика получения продукта из БД
    product = Product(
        id=product_id,
        name="Тестовый продукт",
        description="Описание тестового продукта",
        target_audience="Целевая аудитория",
        platforms=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    generator = ContentGenerator()
    posts = await generator.generate_posts(product, count, tone)
    
    return posts


@router.post("/generate/images")
async def generate_images(
    product_id: int,
    count: int = 3,
    db: Session = Depends(get_db)
):
    """Генерация изображений для продукта"""
    
    product = Product(
        id=product_id,
        name="Тестовый продукт",
        description="Описание тестового продукта",
        target_audience="Целевая аудитория",
        platforms=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    generator = ContentGenerator()
    images = await generator.generate_images(product, count)
    
    return {"images": images}


@router.post("/generate/video-scripts")
async def generate_video_scripts(
    product_id: int,
    count: int = 2,
    db: Session = Depends(get_db)
):
    """Генерация видео-скриптов"""
    
    product = Product(
        id=product_id,
        name="Тестовый продукт",
        description="Описание тестового продукта",
        target_audience="Целевая аудитория",
        platforms=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    generator = ContentGenerator()
    scripts = await generator.generate_video_scripts(product, count)
    
    return {"video_scripts": scripts}


@router.post("/optimize")
async def optimize_content_for_platform(
    post: PostCreate,
    platform: str,
    db: Session = Depends(get_db)
):
    """Оптимизация контента под конкретную платформу"""
    
    generator = ContentGenerator()
    optimized_post = await generator.optimize_content_for_platform(
        post, PlatformType(platform)
    )
    
    return optimized_post


@router.post("/analyze")
async def analyze_content_effectiveness(
    post: PostCreate,
    db: Session = Depends(get_db)
):
    """Анализ эффективности контента"""
    
    generator = ContentGenerator()
    analysis = await generator.analyze_content_effectiveness(post)
    
    return analysis


@router.post("/calendar")
async def generate_content_calendar(
    product_id: int,
    days: int = 30,
    posts_per_day: int = 1,
    db: Session = Depends(get_db)
):
    """Генерация календаря контента"""
    
    product = Product(
        id=product_id,
        name="Тестовый продукт",
        description="Описание тестового продукта",
        target_audience="Целевая аудитория",
        platforms=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    generator = ContentGenerator()
    calendar = await generator.generate_content_calendar(
        product, days, posts_per_day
    )
    
    return {"calendar": calendar}
