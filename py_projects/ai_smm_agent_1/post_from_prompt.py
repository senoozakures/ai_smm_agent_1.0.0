#!/usr/bin/env python3
"""
Интерактивная публикация в Telegram на основе ваших пожеланий.
- Если задан OPENAI_API_KEY, используется AI генерация через ContentGenerator
- Иначе используется простой шаблон на основе введённых данных
"""

import asyncio
from datetime import datetime
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

from app.models.product import Product, PlatformType, ContentType
from app.models.content import PostCreate
from app.services.content.generator import ContentGenerator
from app.services.social.manager import SocialMediaManager


def prompt_non_empty(label: str, default: str = "") -> str:
	value = input(f"{label}{' ['+default+']' if default else ''}: ").strip()
	return value or default


def is_direct_image_url(url: str) -> bool:
	url_l = url.lower()
	return any(url_l.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"))


def build_fallback_post(product_name: str, description: str, audience: str, tone: str) -> str:
	lines: List[str] = []
	lines.append(f"{product_name}: {description}")
	lines.append("")
	lines.append(f"Для: {audience}")
	lines.append(f"Тон: {tone}")
	lines.append("")
	lines.append("Почему это ценно:")
	lines.append("- Практическая польза")
	lines.append("- Понятная подача")
	lines.append("- Экономия времени")
	return "\n".join(lines)


async def main():
	print("🚀 Публикация в Telegram на основе ваших пожеланий")
	print("=" * 60)

	# Проверка Telegram настроек
	bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
	channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
	if not bot_token or not channel_id:
		print("❌ Не настроен Telegram. Укажите TELEGRAM_BOT_TOKEN и TELEGRAM_CHANNEL_ID в .env или через py setup_env.py")
		return

	# Сбор пожеланий
	product_name = prompt_non_empty("Название продукта/услуги", "Онлайн курс по Python")
	description = prompt_non_empty("Короткое описание", "С нуля до реальных проектов")
	audience = prompt_non_empty("Целевая аудитория", "Новички в программировании")
	tone = prompt_non_empty("Тон (friendly, expert, bold...)", "friendly")
	hashtags_raw = input("Хештеги через запятую (опционально): ").strip()
	hashtags = [h.strip() for h in hashtags_raw.split(",") if h.strip()] if hashtags_raw else []
	image_url_input = input("Ссылка на картинку (опционально, прямой URL к .jpg/.png/.webp): ").strip()
	if image_url_input.startswith("@"):
		image_url_input = image_url_input[1:]

	# Создаём продукт и менеджер
	product = Product(
		id=1,
		name=product_name,
		description=description,
		target_audience=audience,
		platforms=[PlatformType.TELEGRAM],
		created_at=datetime.now(),
		updated_at=datetime.now()
	)

	generator = ContentGenerator()
	manager = SocialMediaManager()

	# Получаем текст поста и картинку: через OpenAI (с генерацией изображения) или fallback
	text: str
	всimage_url: str | None = None
	use_ai = bool(os.getenv("OPENAI_API_KEY"))
	if use_ai:
		try:
			# Полная генерация: 1 пост + картинка
			from app.models.content import ContentGenerationRequest
			req = ContentGenerationRequest(
				product_id=product.id,
				content_type=ContentType.POST,
				post_count=1,
				platforms=[PlatformType.TELEGRAM],
				tone=tone,
				include_images=True,
				include_videos=False
			)
			content = await generator.generate_content(product, req)
			post0 = content.posts[0]
			text = post0.text
			image_url = getattr(post0, 'image_url', None)
			if not hashtags:
				hashtags = post0.hashtags
		except Exception as e:
			print(f"⚠️ Не удалось сгенерировать через OpenAI: {e}")
			print("▶ Использую простой шаблон на основе введённых данных")
			text = build_fallback_post(product_name, description, audience, tone)
			image_url = None
	else:
		print("ℹ️ OPENAI_API_KEY не задан — генерирую по простому шаблону")
		text = build_fallback_post(product_name, description, audience, tone)
		image_url = None

	# Если пользователь указал ссылку — используем её приоритетно
	if image_url_input:
		if is_direct_image_url(image_url_input):
			image_url = image_url_input
		else:
			# Не прямой URL на изображение — добавим ссылку в текст, чтобы был превью линка
			text = f"{text}\n\nИсточник изображения: {image_url_input}"

	post = PostCreate(
		product_id=product.id,
		text=text,
		hashtags=hashtags,
		platforms=[PlatformType.TELEGRAM],
		content_type=ContentType.POST,
		image_url=image_url
	)

	print("\n📝 Предпросмотр поста:\n" + "-"*40)
	print(post.text)
	if post.hashtags:
		print("\nХештеги:", ", ".join(post.hashtags))

	confirm = input("\nОпубликовать? (y/N): ").strip().lower()
	if confirm != "y":
		print("❌ Отменено")
		return

	result = await manager.publish_post(post, [PlatformType.TELEGRAM])
	tg = result.get("telegram", {})
	if tg.get("success"):
		print("✅ Опубликовано!")
		if tg.get("url"):
			print("URL:", tg["url"])
	else:
		print("❌ Ошибка публикации:", tg.get("error"))

	print("\nГотово.")


if __name__ == "__main__":
	asyncio.run(main())
