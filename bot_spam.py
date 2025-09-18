import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# === Ваши данные ===
api_id = 123456                # API ID с my.telegram.org
api_hash = 'abcdef1234567890abcdef1234567890'  # API Hash
phone = '+375XXXXXXXXX'        # ваш номер телефона
session_name = 'my_account'    # имя файла сессии

# Группы (chat_id или @username)
TARGETS = [
    -1001234567890,
    '@mygroupusername'
]

MESSAGE_TEXT = "Привет! Это автоматическая рассылка от моего аккаунта."

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start(phone)

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input('Введите код из Telegram: ')
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            pw = input('Введите пароль двухфакторки: ')
            await client.sign_in(password=pw)

    for target in TARGETS:
        try:
            await client.send_message(target, MESSAGE_TEXT)
            print(f"Отправлено в {target}")
        except Exception as e:
            print(f"Ошибка при отправке в {target}: {e}")

if __name__ == '__main__':
    asyncio.run(main())
