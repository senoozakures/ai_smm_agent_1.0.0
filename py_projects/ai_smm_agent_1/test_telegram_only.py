#!/usr/bin/env python3
"""
Тестирование только Telegram функционала без OpenAI

Этот скрипт тестирует Telegram без генерации контента через OpenAI.
"""

import asyncio
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

from app.models.content import PostCreate
from app.models.product import PlatformType
from app.services.social.platforms import TelegramService
from app.services.social.manager import SocialMediaManager


async def test_telegram_connection():
    """Тест подключения к Telegram"""
    print("🔗 Тестирование подключения к Telegram...")
    
    # Проверяем наличие токенов
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    
    if not bot_token or bot_token == "your_telegram_bot_token":
        print("❌ TELEGRAM_BOT_TOKEN не настроен")
        print("   Запустите: py setup_env.py")
        print("   Или добавьте в .env файл: TELEGRAM_BOT_TOKEN=ваш_токен_бота")
        return False
    
    if not channel_id or channel_id == "your_telegram_channel_id":
        print("❌ TELEGRAM_CHANNEL_ID не настроен")
        print("   Запустите: py setup_env.py")
        print("   Или добавьте в .env файл: TELEGRAM_CHANNEL_ID=ваш_id_канала")
        return False
    
    print(f"✅ TELEGRAM_BOT_TOKEN: {'*' * 10}{bot_token[-4:]}")
    print(f"✅ TELEGRAM_CHANNEL_ID: {channel_id}")
    
    # Тестируем подключение
    telegram_service = TelegramService()
    is_connected = await telegram_service.connect()
    
    if is_connected:
        print("✅ Подключение к Telegram успешно!")
        return True
    else:
        print("❌ Не удалось подключиться к Telegram")
        return False


async def test_telegram_posting():
    """Тест публикации в Telegram"""
    print("\n📝 Тестирование публикации в Telegram...")
    
    # Создаем тестовый пост с готовым текстом
    test_post = PostCreate(
        text="🤖 Тестовый пост от SMM AI Agent!\n\nЭто автоматически сгенерированный контент для проверки работы системы.\n\n#SMM #AI #Тест #Автоматизация #Telegram",
        hashtags=["#SMM", "#AI", "#Тест", "#Автоматизация", "#Telegram"],
        platforms=[PlatformType.TELEGRAM],
        product_id=1,
        scheduled_time=None
    )
    
    # Публикуем пост
    telegram_service = TelegramService()
    result = await telegram_service.publish_post(test_post)
    
    print(f"📤 Результат публикации:")
    print(f"   Post ID: {result.get('post_id', 'N/A')}")
    print(f"   URL: {result.get('url', 'N/A')}")
    print(f"   Platform: {result.get('platform', 'N/A')}")
    
    return result


async def test_telegram_analytics():
    """Тест получения аналитики"""
    print("\n📊 Тестирование аналитики Telegram...")
    
    telegram_service = TelegramService()
    analytics = await telegram_service.get_post_analytics("test_post_id")
    
    print(f"📈 Аналитика поста:")
    print(f"   Просмотры: {analytics.get('views', 'N/A')}")
    print(f"   Пересылки: {analytics.get('forwards', 'N/A')}")
    print(f"   Реакции: {analytics.get('reactions', 'N/A')}")
    
    return analytics


async def test_telegram_via_manager():
    """Тест через SocialMediaManager"""
    print("\n🎛️ Тестирование через SocialMediaManager...")
    
    # Создаем тестовый пост
    test_post = PostCreate(
        text="🎯 Второй тестовый пост через менеджер!\n\nПроверяем работу системы управления социальными сетями.\n\n#Тест #Менеджер #SMM #Telegram",
        hashtags=["#Тест", "#Менеджер", "#SMM", "#Telegram"],
        platforms=[PlatformType.TELEGRAM],
        product_id=1,
        scheduled_time=None
    )
    
    # Публикуем через менеджер
    manager = SocialMediaManager()
    results = await manager.publish_post(test_post, [PlatformType.TELEGRAM])
    
    print(f"📤 Результат через менеджер:")
    for platform, result in results.items():
        status = "✅ Успешно" if result.get('success') else "❌ Ошибка"
        print(f"   {platform}: {status}")
        if result.get('error'):
            print(f"      Ошибка: {result['error']}")
        if result.get('url'):
            print(f"      URL: {result['url']}")
    
    return results


async def test_telegram_scheduling():
    """Тест планирования публикаций"""
    print("\n📅 Тестирование планирования публикаций...")
    
    # Создаем тестовый пост для планирования
    test_post = PostCreate(
        text="📅 Запланированный пост!\n\nЭтот пост был запланирован через SMM AI Agent.\n\n#Планирование #Автоматизация #SMM",
        hashtags=["#Планирование", "#Автоматизация", "#SMM"],
        platforms=[PlatformType.TELEGRAM],
        product_id=1,
        scheduled_time=None
    )
    
    manager = SocialMediaManager()
    
    # Тестируем планирование (заглушка)
    print("   Планирование постов работает в демо-режиме")
    print("   В реальной системе посты будут публиковаться по расписанию")
    
    return True


async def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование Telegram функционала SMM AI Agent")
    print("=" * 60)
    
    # Проверяем подключение
    connection_ok = await test_telegram_connection()
    
    if not connection_ok:
        print("\n❌ Не удалось подключиться к Telegram")
        print("\n📋 Инструкции по настройке:")
        print("1. Создайте бота через @BotFather в Telegram")
        print("2. Создайте канал и добавьте бота как администратора")
        print("3. Получите ID канала через @userinfobot")
        print("4. Запустите: py setup_env.py")
        print("5. Добавьте ваши токены")
        return
    
    # Тестируем публикацию
    await test_telegram_posting()
    
    # Тестируем аналитику
    await test_telegram_analytics()
    
    # Тестируем через менеджер
    await test_telegram_via_manager()
    
    # Тестируем планирование
    await test_telegram_scheduling()
    
    print("\n" + "=" * 60)
    print("🎉 Тестирование Telegram завершено!")
    print("\n💡 Для полного тестирования с OpenAI:")
    print("   1. Получите OpenAI API ключ на https://platform.openai.com/")
    print("   2. Запустите: py setup_env.py")
    print("   3. Добавьте OpenAI API ключ")
    print("   4. Запустите: py test_basic.py")
    print("\n🌐 Для запуска API сервера:")
    print("   py run.py")


if __name__ == "__main__":
    # Запускаем тестирование
    asyncio.run(main())
