#!/usr/bin/env python3
"""
Запуск SMM AI Agent

Этот скрипт запускает FastAPI приложение с настройками для разработки.
"""

import uvicorn
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

if __name__ == "__main__":
    # Настройки для запуска
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print("🚀 Запуск SMM AI Agent...")
    print(f"📍 Адрес: http://{host}:{port}")
    print(f"📚 Документация: http://{host}:{port}/docs")
    print(f"🔄 Автоперезагрузка: {'Включена' if reload else 'Отключена'}")
    print("=" * 50)
    
    # Запускаем сервер
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
