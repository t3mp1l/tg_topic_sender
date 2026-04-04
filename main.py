import asyncio
import logging
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError

load_dotenv()

# ─── Конфиг ───────────────────────────────────────────────────────────────────
API_ID      = int(os.getenv("API_ID"))
API_HASH    = os.getenv("API_HASH")
PHONE       = os.getenv("PHONE")
CHAT_ID     = int(os.getenv("CHAT_ID"))
TOPIC_ID    = int(os.getenv("TOPIC_ID"))
DELAY_HOURS = float(os.getenv("DELAY_HOURS", "1"))

TEXTS_FILE  = Path("messages/texts.txt")
PHOTOS_DIR  = Path("messages/photos")
SESSION     = "sender_session"

# ─── Логирование ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def load_texts() -> list[str]:
    """Загружает тексты из файла, разделённые '---'."""
    if not TEXTS_FILE.exists():
        raise FileNotFoundError(f"Файл с текстами не найден: {TEXTS_FILE}")
    raw = TEXTS_FILE.read_text(encoding="utf-8")
    texts = [t.strip() for t in re.split(r"^\s*---\s*$", raw, flags=re.MULTILINE)]
    return [t for t in texts if t]  # убираем пустые


def load_photos() -> list[Path]:
    """Возвращает отсортированный список фото из папки."""
    if not PHOTOS_DIR.exists():
        raise FileNotFoundError(f"Папка с фото не найдена: {PHOTOS_DIR}")
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    photos = sorted(p for p in PHOTOS_DIR.iterdir() if p.suffix.lower() in exts)
    if not photos:
        raise ValueError(f"В папке {PHOTOS_DIR} нет фото")
    return photos


async def send_message(client: TelegramClient, text: str, photo: Path) -> None:
    """Отправляет фото с подписью в нужный топик."""
    await client.send_file(
        entity=CHAT_ID,
        file=str(photo),
        caption=text,
        reply_to=TOPIC_ID,   # reply_to топика = отправка в топик
        parse_mode="html",
    )
    log.info(f"Отправлено: фото={photo.name!r}, текст={text[:40]!r}...")


async def main() -> None:
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.start(phone=PHONE)
    log.info("Авторизация успешна")

    texts  = load_texts()
    photos = load_photos()
    log.info(f"Загружено текстов: {len(texts)}, фото: {len(photos)}")
    log.info(f"Задержка между отправками: {DELAY_HOURS} ч")

    index = 0
    delay_seconds = DELAY_HOURS * 3600

    while True:
        text  = texts[index % len(texts)]
        photo = photos[index % len(photos)]

        try:
            await send_message(client, text, photo)
        except FloodWaitError as e:
            log.warning(f"FloodWait: жду {e.seconds} сек (Telegram ограничение)")
            await asyncio.sleep(e.seconds)
            continue  # повторяем ту же итерацию без инкремента
        except Exception as e:
            log.error(f"Ошибка отправки: {e}")

        index += 1
        log.info(f"Следующая отправка через {DELAY_HOURS} ч. (индекс={index})")
        await asyncio.sleep(delay_seconds)


if __name__ == "__main__":
    asyncio.run(main())
