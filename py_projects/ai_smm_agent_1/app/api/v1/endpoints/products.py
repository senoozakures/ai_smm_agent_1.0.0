from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.product import ProductCreate, Product, ProductUpdate
from app.services.content.generator import ContentGenerator

router = APIRouter()


@router.post("/", response_model=Product)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Создание нового продукта/услуги"""
    
    # Здесь должна быть логика сохранения в БД
    # Пока что возвращаем заглушку
    return Product(
        id=1,
        name=product.name,
        description=product.description,
        target_audience=product.target_audience,
        platforms=product.platforms,
        price=product.price,
        category=product.category,
        keywords=product.keywords,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@router.get("/", response_model=List[Product])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получение списка продуктов"""
    
    # Здесь должна быть логика получения из БД
    # Пока что возвращаем заглушку
    return []


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Получение продукта по ID"""
    
    # Здесь должна быть логика получения из БД
    # Пока что возвращаем заглушку
    raise HTTPException(status_code=404, detail="Продукт не найден")


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Обновление продукта"""
    
    # Здесь должна быть логика обновления в БД
    # Пока что возвращаем заглушку
    raise HTTPException(status_code=404, detail="Продукт не найден")


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Удаление продукта"""
    
    # Здесь должна быть логика удаления из БД
    return {"message": "Продукт удален"}


@router.post("/{product_id}/content-plan")
async def create_content_plan(
    product_id: int,
    content_type: str = "post",
    post_count: int = 5,
    db: Session = Depends(get_db)
):
    """Создание плана контента для продукта"""
    
    # Здесь должна быть логика получения продукта из БД
    # Пока что создаем заглушку
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
    content_plan = await generator.create_content_plan(
        product=product,
        content_type=content_type,
        post_count=post_count
    )
    
    return content_plan
