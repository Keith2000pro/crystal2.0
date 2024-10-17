async def send_message(client, username, text):
    await client.send_message(username, text)


async def join_chat(client, link):
    try:
        await client.join_chat(link)
        print(f"{client.name} успешно присоединился к чату через ссылку {link}.")
    except Exception as e:
        print(f"Ошибка при попытке {client.name} присоединиться к чату: {e}")
