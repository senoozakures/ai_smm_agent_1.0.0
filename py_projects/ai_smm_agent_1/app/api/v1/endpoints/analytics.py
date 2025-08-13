from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, timedelta

from app.core.database import get_db

router = APIRouter()


@router.get("/overview")
async def get_analytics_overview(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """Получение общей аналитики"""
    
    # Здесь должна быть логика получения аналитики из БД
    # Пока что возвращаем заглушку
    
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    return {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "total_posts": 45,
        "total_engagement": 1250,
        "total_reach": 15000,
        "average_engagement_rate": 0.083,
        "top_performing_platform": "instagram",
        "top_performing_post": {
            "id": 123,
            "text": "Лучший пост месяца! 🚀",
            "engagement": 250,
            "reach": 3000
        }
    }


@router.get("/platforms")
async def get_platform_analytics(
    platform: str = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """Получение аналитики по платформам"""
    
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    # Заглушка для демонстрации
    platforms_data = {
        "instagram": {
            "posts": 20,
            "engagement": 800,
            "reach": 10000,
            "engagement_rate": 0.08,
            "followers": 5000
        },
        "facebook": {
            "posts": 15,
            "engagement": 300,
            "reach": 8000,
            "engagement_rate": 0.0375,
            "followers": 3000
        },
        "twitter": {
            "posts": 10,
            "engagement": 150,
            "reach": 2000,
            "engagement_rate": 0.075,
            "followers": 1000
        }
    }
    
    if platform:
        if platform in platforms_data:
            return {
                "platform": platform,
                "period": {"start_date": start_date, "end_date": end_date},
                "data": platforms_data[platform]
            }
        else:
            raise HTTPException(status_code=404, detail="Платформа не найдена")
    
    return {
        "period": {"start_date": start_date, "end_date": end_date},
        "platforms": platforms_data
    }


@router.get("/posts")
async def get_posts_analytics(
    limit: int = 10,
    sort_by: str = "engagement",
    db: Session = Depends(get_db)
):
    """Получение аналитики постов"""
    
    # Заглушка для демонстрации
    posts = [
        {
            "id": 1,
            "text": "Отличный продукт! 🎉",
            "platform": "instagram",
            "published_at": "2024-01-15T10:00:00",
            "engagement": 250,
            "reach": 3000,
            "likes": 200,
            "comments": 30,
            "shares": 20
        },
        {
            "id": 2,
            "text": "Новое поступление товаров! 📦",
            "platform": "facebook",
            "published_at": "2024-01-14T15:30:00",
            "engagement": 180,
            "reach": 2500,
            "likes": 150,
            "comments": 20,
            "shares": 10
        }
    ]
    
    # Сортировка по указанному полю
    if sort_by == "engagement":
        posts.sort(key=lambda x: x["engagement"], reverse=True)
    elif sort_by == "reach":
        posts.sort(key=lambda x: x["reach"], reverse=True)
    elif sort_by == "published_at":
        posts.sort(key=lambda x: x["published_at"], reverse=True)
    
    return {
        "posts": posts[:limit],
        "total_count": len(posts)
    }


@router.get("/trends")
async def get_content_trends(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Получение трендов контента"""
    
    # Заглушка для демонстрации
    trends = {
        "engagement_trend": [
            {"date": "2024-01-01", "value": 50},
            {"date": "2024-01-02", "value": 65},
            {"date": "2024-01-03", "value": 45},
            {"date": "2024-01-04", "value": 80},
            {"date": "2024-01-05", "value": 70}
        ],
        "reach_trend": [
            {"date": "2024-01-01", "value": 1000},
            {"date": "2024-01-02", "value": 1200},
            {"date": "2024-01-03", "value": 900},
            {"date": "2024-01-04", "value": 1500},
            {"date": "2024-01-05", "value": 1300}
        ],
        "top_hashtags": [
            {"hashtag": "#продукт", "usage": 25},
            {"hashtag": "#качество", "usage": 20},
            {"hashtag": "#новинка", "usage": 15},
            {"hashtag": "#скидка", "usage": 12},
            {"hashtag": "#отзывы", "usage": 10}
        ],
        "best_posting_times": [
            {"time": "10:00", "engagement": 85},
            {"time": "15:00", "engagement": 75},
            {"time": "18:00", "engagement": 70},
            {"time": "12:00", "engagement": 65},
            {"time": "20:00", "engagement": 60}
        ]
    }
    
    return {
        "period_days": days,
        "trends": trends
    }


@router.get("/performance")
async def get_performance_metrics(
    metric: str = "engagement_rate",
    db: Session = Depends(get_db)
):
    """Получение метрик производительности"""
    
    metrics = {
        "engagement_rate": {
            "current": 0.083,
            "previous": 0.075,
            "change": "+10.7%",
            "trend": "up"
        },
        "reach": {
            "current": 15000,
            "previous": 12000,
            "change": "+25%",
            "trend": "up"
        },
        "followers_growth": {
            "current": 5000,
            "previous": 4500,
            "change": "+11.1%",
            "trend": "up"
        },
        "post_frequency": {
            "current": 1.5,
            "previous": 1.2,
            "change": "+25%",
            "trend": "up"
        }
    }
    
    if metric in metrics:
        return {
            "metric": metric,
            "data": metrics[metric]
        }
    else:
        raise HTTPException(status_code=400, detail="Метрика не поддерживается")
