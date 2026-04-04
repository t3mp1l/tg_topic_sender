"""
Утилита для получения ID топиков в чате.
Запусти один раз, скопируй нужный TOPIC_ID в .env
"""
import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.channels import GetForumTopicsRequest

load_dotenv()

API_ID   = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE    = os.getenv("PHONE")
SESSION  = "sender_session"


async def main() -> None:
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.start(phone=PHONE)

    # Можно указать username или числовой ID чата
    chat_username = "kgo4455"

    entity = await client.get_entity(chat_username)
    print(f"\nЧат: {entity.title}")
    print(f"CHAT_ID: {entity.id}  (в .env пиши со знаком минус: -{entity.id})\n")

    result = await client(GetForumTopicsRequest(
        channel=entity,
        offset_date=0,
        offset_id=0,
        offset_topic=0,
        limit=100,
    ))

    print(f"{'ID':<10} {'Название топика'}")
    print("-" * 40)
    for topic in result.topics:
        print(f"{topic.id:<10} {topic.title}")

    print("\nСкопируй нужный ID в .env → TOPIC_ID=...")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
