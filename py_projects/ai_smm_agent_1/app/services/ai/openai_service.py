import openai
from typing import List, Dict, Any, Optional
import asyncio
import aiohttp
import json

from app.core.config import settings


class OpenAIService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE

    async def generate_text(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Генерация текста с помощью GPT"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты опытный SMM-специалист и копирайтер. Создавай качественный контент для социальных сетей."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens or self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Ошибка генерации текста: {str(e)}")

    async def generate_social_media_posts(
        self, 
        product_info: Dict[str, Any], 
        count: int = 5,
        tone: str = "professional"
    ) -> List[str]:
        """Генерация постов для социальных сетей"""
        
        prompt = f"""
        Создай {count} развёрнутых постов для социальных сетей на русском языке на основе данных:
        
        Продукт: {product_info.get('name', '')}
        Описание: {product_info.get('description', '')}
        Целевая аудитория: {product_info.get('target_audience', '')}
        Категория: {product_info.get('category', '')}
        Ключевые слова: {', '.join(product_info.get('keywords', []))}
        Тон: {tone}
        
        Стиль и требования к КАЖДОМУ посту:
        - Научно-деловой стиль, академическая манера изложения, ясные определения ключевых терминов
        - Минимум 300 слов; структурируй: краткое введение; 2–3 абзаца аналитики/обоснований; практические рекомендации; вывод
        - Используй эмодзи очень умеренно (0–2 на весь пост)
        - Не добавляй CTA и не зови подписаться — это добавим отдельно
        - Не придумывай ссылки на исследования и источники; при необходимости формулируй без ложных цитат
        
        Формат ответа:
        - Верни ТОЛЬКО тексты постов
        - Разделяй посты строкой: \n---\n
        """
        
        try:
            response = await self.generate_text(prompt)
            if '\n---\n' in response:
                raw_posts = response.split('\n---\n')
            else:
                # fallback: если модель не добавила разделитель, делим по пустым строкам
                raw_posts = [p for p in response.split('\n\n') if p.strip()]
            posts = [post.strip() for post in raw_posts if post.strip()]
            return posts[:count]
        except Exception as e:
            raise Exception(f"Ошибка генерации постов: {str(e)}")

    async def generate_hashtags(self, product_info: Dict[str, Any], count: int = 5) -> List[str]:
        """Генерация релевантных хештегов"""
        
        prompt = f"""
        Создай {count} популярных и релевантных хештегов для продукта:
        
        Продукт: {product_info.get('name', '')}
        Описание: {product_info.get('description', '')}
        Категория: {product_info.get('category', '')}
        
        Требования:
        - Хештеги должны быть популярными в социальных сетях
        - Включи общие хештеги для категории
        - Добавь специфичные хештеги для продукта
        - Без символа # в начале
        
        Верни только хештеги, разделенные запятыми.
        """
        
        try:
            response = await self.generate_text(prompt)
            hashtags = [tag.strip() for tag in response.split(',') if tag.strip()]
            return hashtags[:count]
        except Exception as e:
            raise Exception(f"Ошибка генерации хештегов: {str(e)}")

    async def generate_image_prompt(self, product_info: Dict[str, Any]) -> str:
        """Генерация промпта для создания изображения"""
        
        prompt = f"""
        Создай детальный промпт для генерации изображения на основе продукта:
        
        Продукт: {product_info.get('name', '')}
        Описание: {product_info.get('description', '')}
        Категория: {product_info.get('category', '')}
        
        Требования к промпту:
        - Детальное описание визуального стиля
        - Укажи цвета, композицию, настроение
        - Сделай изображение привлекательным для соцсетей
        - Учти целевую аудиторию: {product_info.get('target_audience', '')}
        
        Верни только промпт для генерации изображения.
        """
        
        try:
            return await self.generate_text(prompt)
        except Exception as e:
            raise Exception(f"Ошибка генерации промпта для изображения: {str(e)}")

    async def generate_video_script(self, product_info: Dict[str, Any]) -> str:
        """Генерация скрипта для видео"""
        
        prompt = f"""
        Создай короткий скрипт для видео (15-30 секунд) на основе продукта:
        
        Продукт: {product_info.get('name', '')}
        Описание: {product_info.get('description', '')}
        Целевая аудитория: {product_info.get('target_audience', '')}
        
        Требования:
        - Скрипт должен быть динамичным и захватывающим
        - Включи призыв к действию
        - Укажи визуальные элементы и переходы
        - Сделай акцент на пользе продукта
        
        Верни только скрипт видео.
        """
        
        try:
            return await self.generate_text(prompt)
        except Exception as e:
            raise Exception(f"Ошибка генерации скрипта видео: {str(e)}")

    async def generate_image(self, prompt: str) -> str:
        """Генерация изображения с помощью DALL-E"""
        try:
            response = await self.client.images.generate(
                model=settings.DALL_E_MODEL,
                prompt=prompt,
                size=settings.DALL_E_SIZE,
                quality=settings.DALL_E_QUALITY,
                n=1
            )
            return response.data[0].url
        except Exception as e:
            raise Exception(f"Ошибка генерации изображения: {str(e)}")

    async def analyze_content_performance(self, post_text: str) -> Dict[str, Any]:
        """Анализ потенциальной эффективности контента"""
        
        prompt = f"""
        Проанализируй следующий пост для социальных сетей и оцени его потенциальную эффективность:
        
        Пост: {post_text}
        
        Оцени по шкале 1-10 следующие параметры:
        - Привлекательность заголовка
        - Читаемость текста
        - Эмоциональное воздействие
        - Призыв к действию
        - Релевантность для аудитории
        
        Верни ответ в формате JSON с оценками и рекомендациями.
        """
        
        try:
            response = await self.generate_text(prompt)
            # Попытка парсинга JSON
            try:
                return json.loads(response)
            except:
                # Если не удалось распарсить JSON, возвращаем текстовый анализ
                return {
                    "analysis": response,
                    "score": 7,  # Средняя оценка
                    "recommendations": ["Проверьте грамматику", "Добавьте больше эмодзи"]
                }
        except Exception as e:
            raise Exception(f"Ошибка анализа контента: {str(e)}")
