import asyncio
import aiofiles

from pyrogram import Client, errors
from colorama import Fore, init
from config import *  # Убедитесь, что ваш конфигурационный файл корректен

# Инициализация colorama
init(autoreset=True)

CHAT_ID = -1002380633194  # Укажите ID чата, в который будут добавляться пользователи
ADDED_USERS_FILE = "./added_users.txt"  # Файл для хранения имен добавленных пользователей
NOT_ADDED_USERS_FILE = "./not_added_users.txt"  # Файл для хранения имен пользователей, которых не удалось добавить
USER_LIST_FILE = "./users.txt"  # Файл для хранения списка пользователей

async def read_users_from_file(file_path):
    """Читает пользователей из файла и возвращает их в виде множества."""
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
            users = {line.strip() for line in await file.readlines() if line.strip()}  # Используем множество для исключения дубликатов
        return users
    except Exception as e:
        print(f"{Fore.RED}Ошибка при чтении файла {file_path}: {e}")
        return set()

async def write_user_to_file(file_path, username):
    """Записывает имя пользователя в файл, если его там еще нет."""
    try:
        # Сначала читаем файл, чтобы проверить наличие пользователя
        existing_users = await read_users_from_file(file_path)
        if username in existing_users:
            print(f"{Fore.YELLOW}Пользователь {username} уже есть в файле {file_path}. Пропускаем запись.")
            return  # Пропускаем запись, если пользователь уже есть

        async with aiofiles.open(file_path, "a", encoding="utf-8") as file:
            await file.write(f"{username}\n")  # Записываем имя пользователя в файл
            print(f"{Fore.LIGHTBLUE_EX}Пользователь {username} записан в файл {file_path}.")  # Отладочное сообщение
    except Exception as e:
        print(f"{Fore.RED}Ошибка при записи в файл {file_path}: {e}")

async def add_users_to_chat(app, usernames, added_users):
    """Добавляет пользователей в чат, учитывая ограничения."""
    for username in usernames:
        if username in added_users:  # Проверяем, добавлен ли пользователь ранее
            print(f"{Fore.YELLOW}Пользователь {username} уже добавлен. Пропускаем...")
            continue  # Пропускаем добавление, если пользователь уже есть в списке

        if not username.startswith('@'):
            username = '@' + username  # Добавляем @, если его нет

        while True:  # Продолжаем пытаться до тех пор, пока не удастся добавить пользователя
            try:
                await app.add_chat_members(CHAT_ID, username)
                print(f"{Fore.GREEN}Пользователь {username} успешно добавлен в чат {CHAT_ID}.")
                await write_user_to_file(ADDED_USERS_FILE, username)  # Записываем пользователя в файл добавленных
                added_users.add(username)  # Добавляем пользователя в множество добавленных
                break  # Выходим из цикла при успешном добавлении
            except errors.FloodWait as e:
                wait_time = e.x  # Получаем время ожидания из исключения FloodWait
                print(f"{Fore.YELLOW}Сработало FloodWait. Ожидание {wait_time} секунд перед сменой аккаунта...")
                await asyncio.sleep(wait_time)  # Ожидание указанное в FloodWait
                return  # Выходим из функции, чтобы переключиться на следующий аккаунт
            except Exception as e:
                print(f"{Fore.RED}Ошибка при добавлении пользователя {username}: {e}")
                await write_user_to_file(NOT_ADDED_USERS_FILE, username)  # Записываем пользователя в файл не добавленных
                break  # Выходим из цикла при ошибке, отличной от FloodWait

async def process_clients(usernames, added_users):
    """Обрабатывает клиентов и добавляет пользователей в чат."""
    for app in apps.values():  # Проходим по каждому клиенту
        try:
            if not app.is_connected:
                print(f"{Fore.YELLOW}Запуск клиента {app.name}...")
                await app.start()

            await asyncio.sleep(2)  # Пауза на 2 секунды перед обработкой

            await add_users_to_chat(app, usernames, added_users)

        except Exception as e:
            print(f"{Fore.RED}Ошибка при обработке клиента {app.name}: {e}")
        finally:
            if app.is_connected:
                print(f"{Fore.YELLOW}Остановка клиента {app.name}...")
                await app.stop()

async def main():
    added_users = await read_users_from_file(ADDED_USERS_FILE)  # Чтение уже добавленных пользователей
    users = await read_users_from_file(USER_LIST_FILE)  # Чтение новых пользователей из users.txt

    # Фильтрация пользователей, оставляя только тех, кто еще не добавлен
    filtered_users = users - added_users

    if not filtered_users:
        print(f"{Fore.YELLOW}Все пользователи уже добавлены. Завершение.")
        return

    while filtered_users:  # Продолжаем попытки добавления пользователей, пока список не станет пустым
        await process_clients(filtered_users, added_users)  # Обработка каждого клиента
        await asyncio.sleep(2)  # Опционально: подождите немного перед повторной попыткой

        # Обновление списка отфильтрованных пользователей после каждой обработки
        filtered_users = users - added_users  # Обновляем список, исключая добавленных пользователей

        # Проверка на наличие оставшихся пользователей
        if not filtered_users:
            print(f"{Fore.YELLOW}Все пользователи были добавлены. Завершение программы.")
            return



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        print(f"{Fore.YELLOW}Завершение работы цикла событий...")
        loop.run_until_complete(loop.shutdown_asyncgens())  # Убедитесь, что все асинхронные генераторы завершены
        loop.close()
