from pyrogram import Client
from database.db import *
import aiohttp, os

apps = {
    "account_1": Client("clients/account_1", 25565955, "ef08c59b70e2ab0ab8731dd2b20ddac5"),
    "account_2": Client("clients/account_2", 26647975, "19bee79986bd132c06ea66f6f641dc3e"),
    "account_3": Client("clients/account_3", 20052802, "7a296138d59e67dfdbc43fdc25380c78"),
    "account_4": Client("clients/account_4", 21164227, "b77a0021c2a501b3ebba5b6d6f87ed7f"),
    "account_5": Client("clients/account_5", 26031042, "8c9be4ed111f4c6f5332b7af92c7f856"),
    "account_6": Client("clients/account_6", 20788917, "8aae58fc7ab8ce4785f8f479011d3596"),
    "account_7": Client("clients/account_7", 20898740, "f79fe2361c9f905a5eb994e8a3d32203"),
    "account_8": Client("clients/account_8", 27107193, "e932ff38261e0fd64a571e61d4b05766"),
}


async def get_country_by_ip(ip_address):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip-api.com/json/{ip_address}") as response:
            if response.status == 200:
                data = await response.json()
                return data.get("country", "Unknown")
    return "Unknown"

async def read_messages_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

async def write_added_users_to_file(users, filename="added_users.txt"):
    with open(filename, 'a', encoding='utf-8') as f:
        for user in users:
            f.write(f"{user}\n")

async def start_client(client):
    try:
        await client.start()
        print(f"{client.name} запущен.")
    except Exception as e:
        print(f"Ошибка при запуске {client.name}: {e}")

async def stop_client(client):
    try:
        await client.stop()
        print(f"{client.name} остановлен.")
    except Exception as e:
        print(f"Ошибка при остановке {client.name}: {e}")



async def get_all_chats(app):
    chats = []
    async for dialog in app.get_dialogs():
        chat = dialog.chat
        chats.append(chat)
        if -1002380633194 in chat.id:
            print(f"{Fore.CYAN}good")


    return chats



async def delete_chat_files(chats):
    for chat in chats:
        filename = f"{chat.title}.txt"
        if os.path.exists(filename):
            os.remove(filename)
            print(f"{Fore.GREEN}Удалён файл: {filename}")
        else:
            print(f"{Fore.RED}Файл не найден: {filename}")