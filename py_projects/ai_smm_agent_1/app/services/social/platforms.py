from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import aiohttp

from app.models.content import PostCreate
from app.core.config import settings


class BaseSocialPlatform(ABC):
    """Базовый класс для работы с социальными платформами"""
    
    def __init__(self):
        self.is_connected = False
    
    @abstractmethod
    async def connect(self) -> bool:
        """Подключение к платформе"""
        pass
    
    @abstractmethod
    async def publish_post(self, post: PostCreate) -> Dict[str, Any]:
        """Публикация поста"""
        pass
    
    @abstractmethod
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Получение аналитики поста"""
        pass
    
    @abstractmethod
    async def delete_post(self, post_id: str) -> bool:
        """Удаление поста"""
        pass
    
    @abstractmethod
    async def update_post(self, post_id: str, new_text: str) -> bool:
        """Обновление поста"""
        pass
    
    async def test_connection(self) -> bool:
        """Тестирование подключения"""
        try:
            return await self.connect()
        except:
            return False


class InstagramService(BaseSocialPlatform):
    """Сервис для работы с Instagram"""
    
    def __init__(self):
        super().__init__()
        self.username = settings.INSTAGRAM_USERNAME
        self.password = settings.INSTAGRAM_PASSWORD
    
    async def connect(self) -> bool:
        """Подключение к Instagram"""
        # Здесь должна быть реальная интеграция с Instagram API
        # Пока что возвращаем заглушку
        if self.username and self.password:
            self.is_connected = True
            return True
        return False
    
    async def publish_post(self, post: PostCreate) -> Dict[str, Any]:
        """Публикация поста в Instagram"""
        if not self.is_connected:
            await self.connect()
        
        # Заглушка для демонстрации
        return {
            "post_id": f"ig_{hash(post.text) % 1000000}",
            "url": f"https://instagram.com/p/{hash(post.text) % 1000000}",
            "platform": "instagram"
        }
    
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Получение аналитики поста в Instagram"""
        # Заглушка для демонстрации
        return {
            "likes": 150,
            "comments": 25,
            "shares": 10,
            "reach": 1000,
            "impressions": 1200
        }
    
    async def delete_post(self, post_id: str) -> bool:
        """Удаление поста из Instagram"""
        # Заглушка для демонстрации
        return True
    
    async def update_post(self, post_id: str, new_text: str) -> bool:
        """Обновление поста в Instagram"""
        # Instagram не поддерживает редактирование постов
        return False


class FacebookService(BaseSocialPlatform):
    """Сервис для работы с Facebook"""
    
    def __init__(self):
        super().__init__()
        self.access_token = settings.FACEBOOK_ACCESS_TOKEN
        self.page_id = settings.FACEBOOK_PAGE_ID
    
    async def connect(self) -> bool:
        """Подключение к Facebook"""
        if self.access_token and self.page_id:
            self.is_connected = True
            return True
        return False
    
    async def publish_post(self, post: PostCreate) -> Dict[str, Any]:
        """Публикация поста в Facebook"""
        if not self.is_connected:
            await self.connect()
        
        # Заглушка для демонстрации
        return {
            "post_id": f"fb_{hash(post.text) % 1000000}",
            "url": f"https://facebook.com/{self.page_id}/posts/{hash(post.text) % 1000000}",
            "platform": "facebook"
        }
    
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Получение аналитики поста в Facebook"""
        # Заглушка для демонстрации
        return {
            "likes": 200,
            "comments": 30,
            "shares": 15,
            "reach": 2000,
            "impressions": 2500
        }
    
    async def delete_post(self, post_id: str) -> bool:
        """Удаление поста из Facebook"""
        # Заглушка для демонстрации
        return True
    
    async def update_post(self, post_id: str, new_text: str) -> bool:
        """Обновление поста в Facebook"""
        # Заглушка для демонстрации
        return True


class TwitterService(BaseSocialPlatform):
    """Сервис для работы с Twitter/X"""
    
    def __init__(self):
        super().__init__()
        self.api_key = settings.TWITTER_API_KEY
        self.api_secret = settings.TWITTER_API_SECRET
        self.access_token = settings.TWITTER_ACCESS_TOKEN
        self.access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    async def connect(self) -> bool:
        """Подключение к Twitter"""
        if all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            self.is_connected = True
            return True
        return False
    
    async def publish_post(self, post: PostCreate) -> Dict[str, Any]:
        """Публикация твита"""
        if not self.is_connected:
            await self.connect()
        
        # Заглушка для демонстрации
        return {
            "post_id": f"tw_{hash(post.text) % 1000000}",
            "url": f"https://twitter.com/user/status/{hash(post.text) % 1000000}",
            "platform": "twitter"
        }
    
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Получение аналитики твита"""
        # Заглушка для демонстрации
        return {
            "likes": 100,
            "retweets": 20,
            "replies": 15,
            "impressions": 800,
            "engagement_rate": 0.05
        }
    
    async def delete_post(self, post_id: str) -> bool:
        """Удаление твита"""
        # Заглушка для демонстрации
        return True
    
    async def update_post(self, post_id: str, new_text: str) -> bool:
        """Обновление твита"""
        # Twitter не поддерживает редактирование твитов
        return False


class TelegramService(BaseSocialPlatform):
    """Сервис для работы с Telegram"""
    
    def __init__(self):
        super().__init__()
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.channel_id = settings.TELEGRAM_CHANNEL_ID
    
    async def connect(self) -> bool:
        """Подключение к Telegram"""
        if self.bot_token and self.channel_id:
            self.is_connected = True
            return True
        return False
    
    async def publish_post(self, post: PostCreate) -> Dict[str, Any]:
        """Публикация поста в Telegram канал"""
        if not self.is_connected:
            await self.connect()
        
        # Формируем текст сообщения + CTA (если задан)
        # Нормализуем хештеги (#prefix)
        normalized_tags = []
        for h in (post.hashtags or []):
            h = h.strip()
            if not h:
                continue
            normalized_tags.append(h if h.startswith('#') else f'#{h}')
        hashtags = " ".join(normalized_tags)
        base_text = post.text if not hashtags else f"{post.text}\n\n{hashtags}"
        # Добавляем CTA ровно один раз в самом конце
        cta_suffix = (getattr(settings, "TELEGRAM_CTA_SUFFIX", None) or "").strip()
        if cta_suffix:
            # Удаляем возможные дубликаты CTA внутри текста
            if base_text.strip().endswith(cta_suffix):
                message_text = base_text
            else:
                # Если CTA уже встречается внутри текста, уберём повторы
                if cta_suffix in base_text:
                    base_text = base_text.replace(cta_suffix, "").rstrip()
                message_text = f"{base_text}\n\n{cta_suffix}"
        else:
            message_text = base_text

        # Определяем метод: sendPhoto если есть image_url, иначе sendMessage
        is_photo = getattr(post, "image_url", None) is not None
        if is_photo:
            api_url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            # Telegram ограничивает caption до ~1024 символов
            caption = message_text
            if len(caption) > 1024:
                caption = caption[:1021] + "..."
            payload = {
                "chat_id": self.channel_id,
                "photo": post.image_url,
                "caption": caption,
                "parse_mode": "HTML",
                "disable_notification": False
            }
        else:
            api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.channel_id,
                "text": message_text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
        
        async with aiohttp.ClientSession() as session:
            async def request_with_retry() -> Dict[str, Any]:
                for attempt in range(3):
                    try:
                        async with session.post(api_url, json=payload, timeout=20) as resp:
                            data = await resp.json()
                            if resp.status == 200 and data.get("ok"):
                                return data
                            # Если ошибка, пробуем повторить (кроме 4xx, кроме rate limit 429)
                            if 400 <= resp.status < 500 and resp.status != 429:
                                raise Exception(f"Telegram API error {resp.status}: {data}")
                    except Exception as e:
                        if attempt == 2:
                            raise e
                        await asyncio.sleep(1.5 * (attempt + 1))
                raise Exception("Failed to send message to Telegram after retries")

            data = await request_with_retry()

        result = data.get("result", {})
        message_id = result.get("message_id")

        # Пытаемся сформировать URL сообщения (если указан username канала вида @channel)
        channel_ref = str(self.channel_id)
        url: Optional[str] = None
        if channel_ref.startswith("@"):
            # username без @
            username = channel_ref[1:]
            if message_id is not None:
                url = f"https://t.me/{username}/{message_id}"
        
        return {
            "post_id": f"tg_{message_id}" if message_id is not None else None,
            "url": url,
            "platform": "telegram"
        }
    
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Получение аналитики поста в Telegram"""
        # Заглушка для демонстрации
        return {
            "views": 500,
            "forwards": 10,
            "reactions": 50
        }
    
    async def delete_post(self, post_id: str) -> bool:
        """Удаление поста из Telegram"""
        # Заглушка для демонстрации
        return True
    
    async def update_post(self, post_id: str, new_text: str) -> bool:
        """Обновление поста в Telegram"""
        # Заглушка для демонстрации
        return True
