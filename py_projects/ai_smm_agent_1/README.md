# SMM AI Agent - Автоматизированный AI-агент для ведения соцсетей и продаж

## Описание

SMM AI Agent - это интеллектуальная система автоматизации социальных сетей, которая помогает создавать и публиковать контент для продвижения продуктов и услуг.

## Возможности

- 🤖 **AI-генерация контента**: Автоматическое создание текстов, изображений и видео-скриптов
- 📱 **Мультиплатформенность**: Поддержка Instagram, Facebook, Twitter, Telegram
- 📅 **Планировщик публикаций**: Автоматическое размещение контента по расписанию
- 📊 **Аналитика**: Отслеживание эффективности публикаций
- 🎯 **Персонализация**: Адаптация контента под целевую аудиторию

## Архитектура

```
smm-agent/
├── app/
│   ├── api/           # FastAPI endpoints
│   ├── core/          # Основные настройки и конфигурация
│   ├── models/        # Pydantic модели
│   ├── services/      # Бизнес-логика
│   │   ├── ai/        # AI сервисы (OpenAI, DALL-E)
│   │   ├── social/    # Интеграции с соцсетями
│   │   └── content/   # Генерация контента
│   ├── database/      # Модели БД и миграции
│   └── utils/         # Вспомогательные функции
├── config/            # Конфигурационные файлы
├── tests/             # Тесты
└── docs/              # Документация
```

## Быстрый старт

### 1. Установка

```bash
# Клонирование репозитория
git clone <repository-url>
cd smm-agent

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка

```bash
# Копирование конфигурации
cp env.example .env

# Редактирование .env файла
# Добавьте ваши API ключи, особенно OPENAI_API_KEY
```

### 3. Тестирование

```bash
# Запуск базовых тестов
python test_basic.py

# Демонстрация возможностей
python example_usage.py
```

### 4. Запуск

```bash
# Способ 1: Через run.py
python run.py

# Способ 2: Через uvicorn
uvicorn app.main:app --reload
```

### 5. Проверка работы

- API: http://localhost:8000
- Документация: http://localhost:8000/docs
- Альтернативная документация: http://localhost:8000/redoc

**Подробные инструкции по установке см. в [INSTALL.md](INSTALL.md)**

## Использование

### 1. Создание продукта/услуги

```python
from app.services.content import ContentGenerator

generator = ContentGenerator()
content_plan = generator.create_content_plan(
    product_name="Курс по программированию",
    description="Онлайн курс для начинающих разработчиков",
    target_audience="Студенты 18-25 лет",
    platforms=["instagram", "facebook"]
)
```

### 2. Генерация контента

```python
# Генерация постов
posts = generator.generate_posts(content_plan, count=5)

# Генерация изображений
images = generator.generate_images(posts)

# Создание видео-скриптов
video_scripts = generator.generate_video_scripts(content_plan)
```

### 3. Публикация в соцсети

```python
from app.services.social import SocialMediaManager

manager = SocialMediaManager()
manager.schedule_posts(posts, schedule="daily")
```

## API Endpoints

- `POST /api/v1/products` - Создание нового продукта
- `POST /api/v1/content/generate` - Генерация контента
- `POST /api/v1/social/schedule` - Планирование публикаций
- `GET /api/v1/analytics` - Получение аналитики

## Конфигурация

Основные настройки находятся в файле `config/settings.py`:

- AI модели и их параметры
- Настройки социальных сетей
- Параметры генерации контента
- Расписание публикаций

## Лицензия

MIT License
