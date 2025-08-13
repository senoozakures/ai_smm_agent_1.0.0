from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

from app.services.ai.openai_service import OpenAIService
from app.core.config import settings
from app.models.content import PostCreate, GeneratedContent, ContentGenerationRequest
from app.models.product import Product, PlatformType, ContentType


class ContentGenerator:
    def __init__(self):
        self.ai_service = OpenAIService()

    async def create_content_plan(
        self,
        product: Product,
        content_type: ContentType = ContentType.POST,
        post_count: int = 5,
        platforms: Optional[List[PlatformType]] = None
    ) -> Dict[str, Any]:
        """Создание плана контента для продукта"""
        
        if platforms is None:
            platforms = product.platforms
            
        return {
            "product_id": product.id,
            "content_type": content_type,
            "post_count": post_count,
            "platforms": platforms,
            "created_at": datetime.now()
        }

    async def generate_content(
        self, 
        product: Product, 
        request: ContentGenerationRequest
    ) -> GeneratedContent:
        """Генерация полного контента для продукта"""
        
        # Подготавливаем информацию о продукте
        product_info = {
            "name": product.name,
            "description": product.description,
            "target_audience": product.target_audience,
            "category": product.category,
            "keywords": product.keywords or [],
            "price": product.price
        }
        
        # Генерируем посты
        post_texts = await self.ai_service.generate_social_media_posts(
            product_info=product_info,
            count=request.post_count,
            tone=request.tone
        )
        
        # Генерируем хештеги
        hashtags = await self.ai_service.generate_hashtags(
            product_info=product_info,
            count=5
        )
        
        # Создаем объекты постов
        posts = []
        for i, text in enumerate(post_texts):
            post = PostCreate(
                product_id=product.id,
                text=text,
                hashtags=hashtags,
                platforms=request.platforms,
                content_type=request.content_type
            )
            posts.append(post)
        
        # Генерируем изображения если требуется
        images = []
        if request.include_images:
            try:
                image_prompt = await self.ai_service.generate_image_prompt(product_info)
            except Exception as e:
                image_prompt = None
                print(f"Ошибка генерации промпта изображения: {e}")
            try:
                if image_prompt:
                    image_url = await self.ai_service.generate_image(image_prompt)
                    images.append(image_url)
                    if posts:
                        posts[0].image_url = image_url
            except Exception as e:
                print(f"Ошибка генерации изображения: {e}")
                # продолжаем без изображения
        
        # Генерируем видео-скрипты если требуется
        video_scripts = []
        if request.include_videos:
            try:
                video_script = await self.ai_service.generate_video_script(product_info)
                video_scripts.append(video_script)
            except Exception as e:
                print(f"Ошибка генерации видео-скрипта: {e}")
        
        return GeneratedContent(
            posts=posts,
            images=images,
            video_scripts=video_scripts,
            hashtags=hashtags
        )

    async def generate_posts(
        self, 
        product: Product, 
        count: int = 5,
        tone: str = "professional"
    ) -> List[PostCreate]:
        """Генерация только постов"""
        
        product_info = {
            "name": product.name,
            "description": product.description,
            "target_audience": product.target_audience,
            "category": product.category,
            "keywords": product.keywords or []
        }
        
        post_texts = await self.ai_service.generate_social_media_posts(
            product_info=product_info,
            count=count,
            tone=tone
        )
        
        hashtags = await self.ai_service.generate_hashtags(
            product_info=product_info,
            count=5
        )
        
        posts = []
        for text in post_texts:
            post = PostCreate(
                product_id=product.id,
                text=text,
                hashtags=hashtags,
                platforms=product.platforms,
                content_type=ContentType.POST
            )
            posts.append(post)
        
        return posts

    async def generate_images(self, product: Product, count: int = 3) -> List[str]:
        """Генерация изображений для продукта"""
        
        product_info = {
            "name": product.name,
            "description": product.description,
            "target_audience": product.target_audience,
            "category": product.category
        }
        
        image_prompt = await self.ai_service.generate_image_prompt(product_info)
        images = []
        
        for _ in range(count):
            try:
                image_url = await self.ai_service.generate_image(image_prompt)
                images.append(image_url)
            except Exception as e:
                print(f"Ошибка генерации изображения: {e}")
        
        return images

    async def generate_video_scripts(self, product: Product, count: int = 2) -> List[str]:
        """Генерация видео-скриптов"""
        
        product_info = {
            "name": product.name,
            "description": product.description,
            "target_audience": product.target_audience
        }
        
        scripts = []
        for _ in range(count):
            try:
                script = await self.ai_service.generate_video_script(product_info)
                scripts.append(script)
            except Exception as e:
                print(f"Ошибка генерации видео-скрипта: {e}")
        
        return scripts

    async def optimize_content_for_platform(
        self, 
        post: PostCreate, 
        platform: PlatformType
    ) -> PostCreate:
        """Оптимизация контента под конкретную платформу"""
        
        platform_optimizations = {
            PlatformType.INSTAGRAM: {
                "max_length": 2200,
                "hashtag_count": 30,
                "emoji_usage": "high"
            },
            PlatformType.FACEBOOK: {
                "max_length": 63206,
                "hashtag_count": 5,
                "emoji_usage": "medium"
            },
            PlatformType.TWITTER: {
                "max_length": 280,
                "hashtag_count": 3,
                "emoji_usage": "medium"
            },
            PlatformType.TELEGRAM: {
                "max_length": 4096,
                "hashtag_count": 10,
                "emoji_usage": "high"
            }
        }
        
        optimization = platform_optimizations.get(platform, {})
        
        # Обрезаем текст если нужно
        if len(post.text) > optimization.get("max_length", 1000):
            post.text = post.text[:optimization["max_length"]-3] + "..."
        
        # Ограничиваем количество хештегов
        max_hashtags = optimization.get("hashtag_count", 5)
        if len(post.hashtags) > max_hashtags:
            post.hashtags = post.hashtags[:max_hashtags]
        
        return post

    async def analyze_content_effectiveness(self, post: PostCreate) -> Dict[str, Any]:
        """Анализ эффективности контента"""
        
        return await self.ai_service.analyze_content_performance(post.text)

    async def generate_content_calendar(
        self, 
        product: Product, 
        days: int = 30,
        posts_per_day: int = 1
    ) -> List[Dict[str, Any]]:
        """Генерация календаря контента"""
        
        total_posts = days * posts_per_day
        posts = await self.generate_posts(product, count=total_posts)
        
        calendar = []
        current_date = datetime.now()
        
        for i, post in enumerate(posts):
            post_date = current_date + timedelta(days=i//posts_per_day)
            post_time = current_date.replace(hour=10, minute=0, second=0, microsecond=0)
            
            calendar.append({
                "date": post_date.date(),
                "time": post_time.time(),
                "post": post,
                "platforms": product.platforms
            })
        
        return calendar
