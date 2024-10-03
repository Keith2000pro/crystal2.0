from pyrogram import Client
import aiofiles

#Par53p
app = Client("xxx", 24421121, "f60f95cceb51346e5b28b1338c7162a6",
        proxy={
            "hostname": "45.86.61.16",       
            "port": 63736,                   
            "scheme": "http",              
            "username": "B3us57G2",
            "password": "3mpRRj3q"
        })

async def get_chat_members(chat_id, filename):
    try:
        # Проверяем доступ к чату
        chat = await app.get_chat(chat_id)
        print(f"Chat title: {chat.title}, Chat ID: {chat.id}")

        async for member in app.get_chat_members(chat_id):
            username = member.user.username
            if username:  # Проверяем, что имя пользователя не None
                async with aiofiles.open(filename, "a") as f:
                    await f.write(f"{username}\n")
    except Exception as e:
        print(f"Error while getting chat members: {e}")

@app.on_message()
async def message_handler(client, message):
    chat_id = message.chat.id
    if message.text == "Салам": 
        await get_chat_members(chat_id, "../s.txt")  # Замените "s.txt" на нужное имя файла
        # await app.add_chat_members("-1002380633194", chat_id)

app.run()
