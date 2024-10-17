import asyncio
from config import *
from methods.send__message import send_message
from pyrogram.errors import FloodWait

USER_LIST_FILE = "./users.txt"
CHAT_ID = -1002351500645

INVITE_LINK = "https://t.me/+x4oTQRrfRatjNmUy"  # Ссылка-приглашение в чат

async def add_members(client, users):
    """Добавляем пользователей в чат через определенный клиент."""
    try:
        await client.add_chat_members(CHAT_ID, users)
        print(f"{client.name} добавил участников: {users}")
    except FloodWait as e:
        print(f"FloodWait у {client.name}: {e.value}s. Переход к следующему аккаунту...")
        return False  # Возвращаем False, чтобы сигнализировать о FloodWait
    except Exception as e:
        print(f"Ошибка у {client.name} при добавлении участников: {e}")
        return True  # Возвращаем True для обработки других исключений

async def main():
    users_to_add = fetch_users_from_db()

    if not users_to_add:
        print("Нет пользователей для добавления.")
        return

    for app_name, client in apps.items():
        await client.start()

        for i in range(0, len(users_to_add), 20):
            batch = users_to_add[i:i + 20]
            result = await add_members(client, batch)  # Добавляем текущую партию участников

            if not result:
                break  # Если произошёл FloodWait, выходим из цикла добавления

            # Обновляем статус добавленных пользователей в базе данных
            for username in batch:
                update_user_status_in_db(username, 1)  # Обновляем статус на 1 (добавлен)

            await asyncio.sleep(1)  # Задержка между партиями, чтобы избежать FloodWait

        await client.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
