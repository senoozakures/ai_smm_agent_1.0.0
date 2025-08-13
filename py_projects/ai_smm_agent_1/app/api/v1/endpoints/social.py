from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.content import PostCreate
from app.models.product import PlatformType
from app.services.social.manager import SocialMediaManager

router = APIRouter()


@router.post("/publish")
async def publish_post(
    post: PostCreate,
    platforms: List[PlatformType],
    db: Session = Depends(get_db)
):
    """Публикация поста в социальные сети"""
    
    manager = SocialMediaManager()
    results = await manager.publish_post(post, platforms)
    
    return results


@router.post("/schedule")
async def schedule_posts(
    posts: List[PostCreate],
    schedule_type: str = "daily",
    platforms: List[PlatformType] = None,
    db: Session = Depends(get_db)
):
    """Планирование публикации постов"""
    
    manager = SocialMediaManager()
    results = await manager.schedule_posts(posts, schedule_type, platforms)
    
    return results


@router.post("/scheduler/start")
async def start_scheduler():
    """Запуск планировщика публикаций"""
    
    manager = SocialMediaManager()
    manager.start_scheduler()
    
    return {"message": "Планировщик запущен"}


@router.post("/scheduler/stop")
async def stop_scheduler():
    """Остановка планировщика публикаций"""
    
    manager = SocialMediaManager()
    manager.stop_scheduler()
    
    return {"message": "Планировщик остановлен"}


@router.get("/analytics/{platform}/{post_id}")
async def get_post_analytics(
    platform: PlatformType,
    post_id: str,
    db: Session = Depends(get_db)
):
    """Получение аналитики поста"""
    
    manager = SocialMediaManager()
    analytics = await manager.get_analytics(platform, post_id)
    
    return analytics


@router.delete("/posts/{platform}/{post_id}")
async def delete_post(
    platform: PlatformType,
    post_id: str,
    db: Session = Depends(get_db)
):
    """Удаление поста"""
    
    manager = SocialMediaManager()
    success = await manager.delete_post(platform, post_id)
    
    if success:
        return {"message": "Пост удален"}
    else:
        raise HTTPException(status_code=400, detail="Не удалось удалить пост")


@router.put("/posts/{platform}/{post_id}")
async def update_post(
    platform: PlatformType,
    post_id: str,
    new_text: str,
    db: Session = Depends(get_db)
):
    """Обновление поста"""
    
    manager = SocialMediaManager()
    success = await manager.update_post(platform, post_id, new_text)
    
    if success:
        return {"message": "Пост обновлен"}
    else:
        raise HTTPException(status_code=400, detail="Не удалось обновить пост")


@router.get("/platforms")
async def get_supported_platforms():
    """Получение списка поддерживаемых платформ"""
    
    manager = SocialMediaManager()
    platforms = manager.get_supported_platforms()
    
    return {"platforms": [p.value for p in platforms]}


@router.post("/test-connection/{platform}")
async def test_platform_connection(
    platform: PlatformType,
    db: Session = Depends(get_db)
):
    """Тестирование подключения к платформе"""
    
    manager = SocialMediaManager()
    is_connected = await manager.test_connection(platform)
    
    return {
        "platform": platform.value,
        "connected": is_connected
    }
