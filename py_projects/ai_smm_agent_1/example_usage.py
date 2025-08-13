#!/usr/bin/env python3
"""
Пример использования SMM AI Agent

Этот скрипт демонстрирует основные возможности AI-агента для автоматизации социальных сетей.
"""

import asyncio
from datetime import datetime

from app.models.product import ProductCreate, Product, PlatformType, ContentType
from app.models.content import ContentGenerationRequest
from app.services.content.generator import ContentGenerator
from app.services.social.manager import SocialMediaManager


async def main():
    """Основная функция демонстрации"""
    
    print("🚀 SMM AI Agent - Демонстрация возможностей")
    print("=" * 50)
    
    # 1. Создание продукта
    print("\n1. Создание продукта/услуги...")
    product_data = ProductCreate(
        name="Онлайн курс по программированию Python",
        description="Полный курс для начинающих разработчиков с нуля до создания реальных проектов",
        target_audience="Студенты 18-25 лет, начинающие программисты",
        platforms=[PlatformType.INSTAGRAM, PlatformType.FACEBOOK, PlatformType.TELEGRAM],
        price=299.99,
        category="Образование",
        keywords=["python", "программирование", "курс", "обучение", "разработка"]
    )
    
    print(f"✅ Продукт создан: {product_data.name}")
    
    # 2. Генерация контента
    print("\n2. Генерация контента...")
    
    # Создаем заглушку продукта для демонстрации
    product = Product(
        id=1,
        name=product_data.name,
        description=product_data.description,
        target_audience=product_data.target_audience,
        platforms=product_data.platforms,
        price=product_data.price,
        category=product_data.category,
        keywords=product_data.keywords,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    generator = ContentGenerator()
    
    # Генерируем посты
    print("   Генерация постов...")
    posts = await generator.generate_posts(product, count=3, tone="friendly")
    
    for i, post in enumerate(posts, 1):
        print(f"   Пост {i}: {post.text[:100]}...")
    
    # Генерируем хештеги
    print("   Генерация хештегов...")
    hashtags = await generator.generate_hashtags(
        {
            "name": product.name,
            "description": product.description,
            "category": product.category
        },
        count=5
    )
    print(f"   Хештеги: {', '.join(hashtags)}")
    
    # 3. Планирование публикаций
    print("\n3. Планирование публикаций...")
    
    social_manager = SocialMediaManager()
    
    # Публикуем один пост для демонстрации
    if posts:
        print("   Публикация поста...")
        result = await social_manager.publish_post(posts[0], [PlatformType.INSTAGRAM])
        print(f"   Результат: {result}")
    
    # 4. Анализ эффективности
    print("\n4. Анализ эффективности контента...")
    
    if posts:
        analysis = await generator.analyze_content_effectiveness(posts[0])
        print(f"   Оценка эффективности: {analysis.get('score', 'N/A')}/10")
    
    # 5. Генерация календаря контента
    print("\n5. Генерация календаря контента...")
    
    calendar = await generator.generate_content_calendar(product, days=7, posts_per_day=1)
    print(f"   Создан календарь на {len(calendar)} дней")
    
    # 6. Тестирование подключений к платформам
    print("\n6. Тестирование подключений к платформам...")
    
    platforms = social_manager.get_supported_platforms()
    for platform in platforms:
        is_connected = await social_manager.test_connection(platform)
        status = "✅ Подключено" if is_connected else "❌ Не подключено"
        print(f"   {platform.value}: {status}")
    
    print("\n" + "=" * 50)
    print("🎉 Демонстрация завершена!")
    print("\nДля запуска полного API сервера выполните:")
    print("uvicorn app.main:app --reload")
    print("\nДокументация API будет доступна по адресу:")
    print("http://localhost:8000/docs")


if __name__ == "__main__":
    # Запускаем демонстрацию
    asyncio.run(main())
