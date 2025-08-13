# Инструкции по установке SMM AI Agent

## Требования

- Python 3.8+
- pip (менеджер пакетов Python)
- Git

## Пошаговая установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd smm-agent
```

### 2. Создание виртуального окружения

**Windows:**
```bash
py -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

1. Скопируйте файл конфигурации:
```bash
cp env.example .env
```

2. Отредактируйте файл `.env` и добавьте ваши API ключи:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./smm_agent.db

# Redis Configuration (опционально)
REDIS_URL=redis://localhost:6379

# Social Media API Keys
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
FACEBOOK_ACCESS_TOKEN=your_token
FACEBOOK_PAGE_ID=your_page_id
# ... другие ключи
```

### 5. Получение API ключей

#### OpenAI API Key
1. Зарегистрируйтесь на [OpenAI](https://platform.openai.com/)
2. Перейдите в раздел API Keys
3. Создайте новый ключ
4. Скопируйте ключ в `.env` файл

#### Instagram API
- Используйте Instagram Basic Display API или Graph API
- Для тестирования можно использовать заглушки

#### Facebook API
1. Создайте приложение на [Facebook Developers](https://developers.facebook.com/)
2. Получите Access Token
3. Добавьте Page ID

#### Twitter API
1. Зарегистрируйтесь на [Twitter Developer Portal](https://developer.twitter.com/)
2. Создайте приложение
3. Получите API ключи

#### Telegram Bot
1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Добавьте ID канала

### 6. Запуск приложения

#### Способ 1: Через run.py
```bash
python run.py
```

#### Способ 2: Через uvicorn
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Проверка работы

1. Откройте браузер и перейдите по адресу: `http://localhost:8000`
2. Документация API: `http://localhost:8000/docs`
3. Альтернативная документация: `http://localhost:8000/redoc`

## Тестирование

### Запуск демонстрации
```bash
python example_usage.py
```

### Тестирование API
```bash
# Создание продукта
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тестовый продукт",
    "description": "Описание продукта",
    "target_audience": "Целевая аудитория",
    "platforms": ["instagram", "facebook"],
    "category": "Тест"
  }'
```

## Структура проекта

```
smm-agent/
├── app/                    # Основной код приложения
│   ├── api/               # API endpoints
│   ├── core/              # Конфигурация и настройки
│   ├── models/            # Pydantic модели
│   └── services/          # Бизнес-логика
│       ├── ai/            # AI сервисы
│       ├── content/       # Генерация контента
│       └── social/        # Социальные сети
├── config/                # Конфигурационные файлы
├── tests/                 # Тесты
├── requirements.txt       # Зависимости
├── run.py                 # Скрипт запуска
├── example_usage.py       # Пример использования
└── README.md              # Документация
```

## Возможные проблемы

### Ошибка импорта модулей
```bash
# Убедитесь, что виртуальное окружение активировано
# и зависимости установлены
pip install -r requirements.txt
```

### Ошибка подключения к OpenAI
- Проверьте правильность API ключа
- Убедитесь, что у вас есть доступ к API
- Проверьте баланс аккаунта

### Ошибки с социальными сетями
- Проверьте правильность API ключей
- Убедитесь, что приложения настроены правильно
- Для тестирования используйте заглушки

## Разработка

### Добавление новой платформы
1. Создайте новый класс в `app/services/social/platforms.py`
2. Наследуйтесь от `BaseSocialPlatform`
3. Реализуйте все абстрактные методы
4. Добавьте платформу в `SocialMediaManager`

### Добавление новых типов контента
1. Добавьте новый тип в `ContentType` enum
2. Обновите логику генерации в `ContentGenerator`
3. Добавьте соответствующие API endpoints

## Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Убедитесь, что все зависимости установлены
3. Проверьте правильность конфигурации
4. Создайте issue в репозитории проекта
