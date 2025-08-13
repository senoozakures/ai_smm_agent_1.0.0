#!/usr/bin/env python3
"""
Базовые тесты для SMM AI Agent

Этот файл содержит простые тесты для проверки работы основных компонентов.
"""

import asyncio
import sys
import os

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.product import ProductCreate, PlatformType
from app.services.content.generator import ContentGenerator
from app.services.social.manager import SocialMediaManager


async def test_content_generation():
    """Тест генерации контента"""
    print("🧪 Тестирование генерации контента...")
    
    try:
        # Создаем тестовый продукт
        product_data = {
            "name": "Тестовый продукт",
            "description": "Описание тестового продукта",
            "target_audience": "Тестовая аудитория",
            "category": "Тест",
            "keywords": ["тест", "продукт"]
        }
        
        # Тестируем генерацию постов (которые включают хештеги)
        generator = ContentGenerator()
        # Создаем заглушку продукта для тестирования
        from app.models.product import Product
        from datetime import datetime
        
        test_product = Product(
            id=1,
            name=product_data["name"],
            description=product_data["description"],
            target_audience=product_data["target_audience"],
            category=product_data["category"],
            keywords=product_data["keywords"],
            platforms=[],
            price=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        posts = await generator.generate_posts(test_product, count=1)
        
        assert len(posts) > 0, "Посты не были сгенерированы"
        print(f"✅ Посты сгенерированы: {len(posts)} шт.")
        print(f"✅ Хештеги в первом посте: {posts[0].hashtags}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тесте генерации контента: {e}")
        return False


async def test_social_media_manager():
    """Тест менеджера социальных сетей"""
    print("🧪 Тестирование менеджера социальных сетей...")
    
    try:
        manager = SocialMediaManager()
        platforms = manager.get_supported_platforms()
        
        assert len(platforms) > 0, "Нет поддерживаемых платформ"
        print(f"✅ Поддерживаемые платформы: {[p.value for p in platforms]}")
        
        # Тестируем подключение к платформам
        for platform in platforms:
            is_connected = await manager.test_connection(platform)
            status = "✅" if is_connected else "❌"
            print(f"   {status} {platform.value}: {'Подключено' if is_connected else 'Не подключено'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тесте менеджера соцсетей: {e}")
        return False


async def test_models():
    """Тест моделей данных"""
    print("🧪 Тестирование моделей данных...")
    
    try:
        # Тестируем создание продукта
        product = ProductCreate(
            name="Тестовый продукт",
            description="Описание",
            target_audience="Аудитория",
            platforms=[PlatformType.INSTAGRAM, PlatformType.FACEBOOK],
            category="Тест"
        )
        
        assert product.name == "Тестовый продукт", "Неправильное имя продукта"
        assert len(product.platforms) == 2, "Неправильное количество платформ"
        
        print("✅ Модели данных работают корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тесте моделей: {e}")
        return False


async def run_all_tests():
    """Запуск всех тестов"""
    print("🚀 Запуск тестов SMM AI Agent")
    print("=" * 40)
    
    tests = [
        test_models,
        test_content_generation,
        test_social_media_manager
    ]
    
    results = []
    
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Критическая ошибка в тесте {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 40)
    print("📊 Результаты тестов:")
    
    passed = sum(results)
    total = len(results)
    
    for i, result in enumerate(results):
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"   Тест {i+1}: {status}")
    
    print(f"\n🎯 Итого: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены успешно!")
        return True
    else:
        print("⚠️  Некоторые тесты не пройдены")
        return False


if __name__ == "__main__":
    # Запускаем тесты
    success = asyncio.run(run_all_tests())
    
    if success:
        print("\n✅ Система готова к работе!")
        print("Запустите приложение командой: python run.py")
    else:
        print("\n❌ Обнаружены проблемы в системе")
        print("Проверьте конфигурацию и зависимости")
    
    sys.exit(0 if success else 1)
