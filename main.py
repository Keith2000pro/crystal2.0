import asyncio
from database.db import *

USER_LIST_FILE = "./users.txt"


async def main():
    # Чтение пользователей из файла и вставка их в базу данных
    users = await read_users_from_file(USER_LIST_FILE)
    if not users:
        print("Файл пользователей пуст или не найден.")
        return
    for username in users:
        insert_user_into_db(username)

    # Чтение пользователей из базы данных и обновление их статуса
    pending_users = fetch_users_from_db()
    if not pending_users:
        print("Нет пользователей со статусом 0 для обновления.")
        return

    for username in pending_users:
        # Ваши действия с пользователем, например, добавление в чат
        update_user_status_in_db(username, 0)  # Обновление статуса на 1 после обработки

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
