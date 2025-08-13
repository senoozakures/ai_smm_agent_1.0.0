#!/usr/bin/env python3
"""
Скрипт для настройки переменных окружения SMM AI Agent

Этот скрипт поможет настроить необходимые API ключи для работы системы.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Создание .env файла с настройками"""
    
    env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./smm_agent.db

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Social Media API Keys

# Instagram
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Facebook
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# Twitter/X
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_telegram_channel_id

# Application Settings
LOG_LEVEL=INFO
ALLOWED_HOSTS=["*"]
"""
    
    env_path = Path(".env")
    
    if env_path.exists():
        print("⚠️  Файл .env уже существует!")
        response = input("Перезаписать? (y/N): ").lower()
        if response != 'y':
            print("❌ Отменено")
            return False
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Файл .env создан успешно!")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания файла .env: {e}")
        return False

def update_env_value(key, value):
    """Обновление значения в .env файле"""
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ Файл .env не найден. Сначала создайте его.")
        return False
    
    try:
        # Читаем текущий файл
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Ищем и обновляем ключ
        updated = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                updated = True
                break
        
        if not updated:
            print(f"❌ Ключ {key} не найден в .env файле")
            return False
        
        # Записываем обновленный файл
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"✅ {key} обновлен успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления {key}: {e}")
        return False

def interactive_setup():
    """Интерактивная настройка API ключей"""
    
    print("🚀 Настройка SMM AI Agent")
    print("=" * 40)
    
    # Создаем .env файл если его нет
    if not Path(".env").exists():
        if not create_env_file():
            return
    
    print("\n📝 Настройка API ключей:")
    print("(Нажмите Enter чтобы пропустить)")
    
    # OpenAI API Key
    openai_key = input("\n🔑 OpenAI API Key (sk-...): ").strip()
    if openai_key and openai_key != "your_openai_api_key_here":
        update_env_value("OPENAI_API_KEY", openai_key)
    
    # Telegram Bot Token
    telegram_token = input("\n🤖 Telegram Bot Token: ").strip()
    if telegram_token and telegram_token != "your_telegram_bot_token":
        update_env_value("TELEGRAM_BOT_TOKEN", telegram_token)
    
    # Telegram Channel ID
    telegram_channel = input("\n📢 Telegram Channel ID (-100...): ").strip()
    if telegram_channel and telegram_channel != "your_telegram_channel_id":
        update_env_value("TELEGRAM_CHANNEL_ID", telegram_channel)
    
    print("\n✅ Настройка завершена!")
    print("\n💡 Теперь вы можете запустить тесты:")
    print("   py test_telegram.py")
    print("   py test_basic.py")

def show_current_settings():
    """Показать текущие настройки"""
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ Файл .env не найден")
        return
    
    print("📋 Текущие настройки:")
    print("=" * 40)
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if 'key' in key.lower() or 'token' in key.lower():
                        # Скрываем чувствительные данные
                        if value and value != 'your_openai_api_key_here':
                            masked_value = '*' * (len(value) - 4) + value[-4:]
                            print(f"{key}: {masked_value}")
                        else:
                            print(f"{key}: {value}")
                    else:
                        print(f"{key}: {value}")
    except Exception as e:
        print(f"❌ Ошибка чтения .env файла: {e}")

def main():
    """Основная функция"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "create":
            create_env_file()
        elif command == "show":
            show_current_settings()
        elif command == "update":
            if len(sys.argv) >= 4:
                key = sys.argv[2]
                value = sys.argv[3]
                update_env_value(key, value)
            else:
                print("❌ Использование: py setup_env.py update KEY VALUE")
        else:
            print("❌ Неизвестная команда")
            print("Доступные команды: create, show, update")
    else:
        interactive_setup()

if __name__ == "__main__":
    main()
