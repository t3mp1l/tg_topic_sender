# Telegram Topic Sender

Юзербот на Telethon, который по расписанию постит сообщения (текст + при необходимости фото) в конкретную тему форума супергруппы, с фиксированной паузой между отправками.

Личная автоматизация. Использовать только со своим аккаунтом и в группах, где ты админ.

## Возможности

Постит именно в нужную тему форума (по `message_thread_id`), по кругу берёт сообщения из `messages/texts.txt` с настраиваемой задержкой между отправками. Умеет прикладывать фото из `messages/photos`. Корректно переживает `FloodWaitError`. В комплекте `get_topic_id.py` — помощник, чтобы узнать id чата и темы.

## Запуск

```bash
pip install -r requirements.txt
cp .env.example .env      # API_ID, API_HASH, PHONE, CHAT_ID, TOPIC_ID, DELAY_HOURS

python get_topic_id.py    # если не знаешь id чата/темы
python main.py
```

`API_ID` и `API_HASH` берутся на https://my.telegram.org. Файл сессии создаётся локально при первом запуске и лежит в `.gitignore`.

## Переменные

`API_ID`, `API_HASH`, `PHONE`, `CHAT_ID`, `TOPIC_ID`, `DELAY_HOURS` (можно дробное, например `1.5`). Тексты — в `messages/texts.txt`, фото — в `messages/photos/`.

## Лицензия

MIT.
