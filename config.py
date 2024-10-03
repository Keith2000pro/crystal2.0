from pyrogram import Client
from database.database import *
import aiohttp, os

apps = {
    "Veraty2200": Client(
                "clients/my_account0",               # Путь к сессии
                24421121,                             # API ID
                "f60f95cceb51346e5b28b1338c7162a6",  # API Hash
                proxy={
                    "hostname": "45.138.4.15",       
                    "port": 63500,                   
                    "scheme": "http",              
                    "username": "B3us57G2",
                    "password": "3mpRRj3q"
                }
            ),
    # "xxx": Client(
    #             "clients/xxx",               
    #             24421121,                             
    #             "f60f95cceb51346e5b28b1338c7162a6",  
    #             proxy={
    #                 "hostname": "45.138.4.15",       
    #                 "port": 63500,                   
    #                 "scheme": "http",              
    #                 "username": "B3us57G2",
    #                 "password": "3mpRRj3q"
    #             }
    #         ),
    "Focys_00": Client(
        "clients/my_account1", 25343396, "1a5633a3b2fbf9bf36c122bf1d9b6e9f",
        proxy={
                    "hostname": "185.246.220.176",       
                    "port": 64412,                   
                    "scheme": "http",              
                    "username": "B3us57G2",
                    "password": "3mpRRj3q"
        }),

    "Jdjfjjfghh": Client("clients/my_account2", 24025578, "b2d621697eaf188864f8df3f2c090e04",
        proxy={
                    "hostname": "178.130.56.207",       
                    "port": 62730,                   
                    "scheme": "http",              
                    "username": "B3us57G2",
                    "password": "3mpRRj3q"
        }),

    "good_Iike": Client("clients/my_account3", 27848721, "361a88c26010925fefbc01b18baf792e",
        proxy={
                    "hostname": "45.138.4.15",       
                    "port": 63500,                   
                    "scheme": "http",              
                    "username": "B3us57G2",
                    "password": "3mpRRj3q"
                }),

    "Iadycrystall": Client("clients/my_account4", 26664469, "5de0fd086d39de0dc8f55583ade9b770",
        proxy={
                    "hostname": "45.199.227.116",       
                    "port": 63623,                   
                    "scheme": "http",              
                    "username": "B3us57G2",
                    "password": "3mpRRj3q"
        }),

    "LOVEhjdn": Client(
        "clients/my_account5", 21527337, "498d2702d39edc6a99ecec65b3622a1b",
        proxy={
            "hostname": "194.107.200.151",       
            "port": 63195,                   
            "scheme": "http",              
            "username": "B3us57G2",
            "password": "3mpRRj3q"
            }),

    "My_loveroud": Client("clients/my_account6", 26637833, "3f186327212d01e2941d1efd211a3c7c",
        proxy={
            "hostname": "45.138.4.15",       
            "port": 63500,                   
            "scheme": "http",              
            "username": "B3us57G2",
            "password": "3mpRRj3q"
        }),
    "ocknfbd": Client("clients/my_account7", 28196244, "ea0a55baf144b7d7969609d2c6f36922",
        proxy={
            "hostname": "45.138.4.15",       
            "port": 63500,                   
            "scheme": "http",              
            "username": "B3us57G2",
            "password": "3mpRRj3q"
        }),
    "djjdjdndkd6": Client("clients/my_account8", 23033281, "05b6275795ae899dd9016339baa43014",
        proxy={
            "hostname": "45.138.4.15",       
            "port": 63500,                   
            "scheme": "http",              
            "username": "B3us57G2",
            "password": "3mpRRj3q"
        }),
    "plxnbbs": Client("clients/my_account9", 29622314, "df404a2af9d721d8406b0863c759f000",
        proxy={
            "hostname": "45.138.4.15",       
            "port": 63500,                   
            "scheme": "http",              
            "username": "B3us57G2",
            "password": "3mpRRj3q"
        }),
        
    "n_nxndjdjf": Client("clients/my_account10", 29638259, "9c564280c37eac5f048f40fd7d779602",
        proxy={
            "hostname": "45.138.4.15",       
            "port": 63500,                   
            "scheme": "http",              
            "username": "B3us57G2",
            "password": "3mpRRj3q"
        }),

    # "kckciviv": Client("clients/my_account11", 27017136, "d427423621141d6fb624a8d20867c57b",
    #     proxy={
    #         "hostname": "45.138.4.15",       
    #         "port": 63500,                   
    #         "scheme": "http",              
    #         "username": "B3us57G2",
    #         "password": "3mpRRj3q"
    #     }),
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