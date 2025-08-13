from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
import schedule
import time
from threading import Thread

from app.models.content import PostCreate, PostStatus
from app.models.product import PlatformType
from app.core.config import settings
from app.services.social.platforms import (
    InstagramService,
    FacebookService,
    TwitterService,
    TelegramService
)


class SocialMediaManager:
    def __init__(self):
        self.platforms = {
            PlatformType.INSTAGRAM: InstagramService(),
            PlatformType.FACEBOOK: FacebookService(),
            PlatformType.TWITTER: TwitterService(),
            PlatformType.TELEGRAM: TelegramService()
        }
        self.scheduler_thread = None
        self.is_running = False

    async def publish_post(self, post: PostCreate, platforms: List[PlatformType]) -> Dict[str, Any]:
        """Публикация поста в указанные платформы"""
        
        results = {}
        
        for platform in platforms:
            if platform in self.platforms:
                try:
                    service = self.platforms[platform]
                    result = await service.publish_post(post)
                    results[platform.value] = {
                        "success": True,
                        "post_id": result.get("post_id"),
                        "url": result.get("url")
                    }
                except Exception as e:
                    results[platform.value] = {
                        "success": False,
                        "error": str(e)
                    }
            else:
                results[platform.value] = {
                    "success": False,
                    "error": f"Платформа {platform.value} не поддерживается"
                }
        
        return results

    async def schedule_posts(
        self, 
        posts: List[PostCreate], 
        schedule_type: str = "daily",
        platforms: Optional[List[PlatformType]] = None
    ) -> Dict[str, Any]:
        """Планирование публикации постов"""
        
        if platforms is None:
            platforms = [PlatformType.INSTAGRAM, PlatformType.FACEBOOK]
        
        scheduled_posts = []
        
        for i, post in enumerate(posts):
            # Определяем время публикации
            if schedule_type == "daily":
                publish_time = datetime.now().replace(
                    hour=10, minute=0, second=0, microsecond=0
                )
                publish_time = publish_time.replace(day=publish_time.day + i)
            elif schedule_type == "weekly":
                publish_time = datetime.now().replace(
                    hour=10, minute=0, second=0, microsecond=0
                )
                publish_time = publish_time.replace(day=publish_time.day + (i * 7))
            else:
                publish_time = datetime.now()
            
            scheduled_post = {
                "post": post,
                "publish_time": publish_time,
                "platforms": platforms,
                "status": PostStatus.SCHEDULED
            }
            
            scheduled_posts.append(scheduled_post)
            
            # Добавляем в планировщик
            self._add_to_scheduler(scheduled_post)
        
        return {
            "scheduled_count": len(scheduled_posts),
            "schedule_type": schedule_type,
            "posts": scheduled_posts
        }

    def _add_to_scheduler(self, scheduled_post: Dict[str, Any]):
        """Добавление поста в планировщик"""
        
        publish_time = scheduled_post["publish_time"]
        post = scheduled_post["post"]
        platforms = scheduled_post["platforms"]
        
        # Планируем публикацию
        schedule.every().day.at(publish_time.strftime("%H:%M")).do(
            self._publish_scheduled_post, post, platforms
        )

    async def _publish_scheduled_post(self, post: PostCreate, platforms: List[PlatformType]):
        """Публикация запланированного поста"""
        
        try:
            results = await self.publish_post(post, platforms)
            
            # Обновляем статус поста
            post.status = PostStatus.PUBLISHED
            post.published_at = datetime.now()
            
            return results
        except Exception as e:
            post.status = PostStatus.FAILED
            raise e

    def start_scheduler(self):
        """Запуск планировщика в отдельном потоке"""
        
        if not self.is_running:
            self.is_running = True
            self.scheduler_thread = Thread(target=self._run_scheduler)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()

    def stop_scheduler(self):
        """Остановка планировщика"""
        
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()

    def _run_scheduler(self):
        """Запуск планировщика"""
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту

    async def get_analytics(self, platform: PlatformType, post_id: str) -> Dict[str, Any]:
        """Получение аналитики поста"""
        
        if platform in self.platforms:
            service = self.platforms[platform]
            return await service.get_post_analytics(post_id)
        else:
            raise ValueError(f"Платформа {platform.value} не поддерживается")

    async def delete_post(self, platform: PlatformType, post_id: str) -> bool:
        """Удаление поста"""
        
        if platform in self.platforms:
            service = self.platforms[platform]
            return await service.delete_post(post_id)
        else:
            raise ValueError(f"Платформа {platform.value} не поддерживается")

    async def update_post(self, platform: PlatformType, post_id: str, new_text: str) -> bool:
        """Обновление поста"""
        
        if platform in self.platforms:
            service = self.platforms[platform]
            return await service.update_post(post_id, new_text)
        else:
            raise ValueError(f"Платформа {platform.value} не поддерживается")

    def get_supported_platforms(self) -> List[PlatformType]:
        """Получение списка поддерживаемых платформ"""
        
        return list(self.platforms.keys())

    async def test_connection(self, platform: PlatformType) -> bool:
        """Тестирование подключения к платформе"""
        
        if platform in self.platforms:
            service = self.platforms[platform]
            return await service.test_connection()
        else:
            return False
