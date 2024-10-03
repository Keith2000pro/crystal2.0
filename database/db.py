import pymysql

DB_HOST = "localhost"
DB_USER = "engel"
DB_PASSWORD = "61218389"
DB_NAME = "crystal"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

async def read_users_from_file(file_path):
    """Читает пользователей из файла и возвращает их в виде списка."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            users = [line.strip() for line in file if line.strip()]
        return users
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return []

def insert_user_into_db(username):
    """Вставляет пользователя в базу данных."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (username, status) VALUES (%s, %s)"
            cursor.execute(sql, (username, 0))  # Добавляем пользователя со статусом "0"
            connection.commit()
            print(f"Пользователь {username} успешно добавлен в базу данных.")
    except pymysql.MySQLError as e:
        print(f"Ошибка при добавлении пользователя {username} в базу данных: {e}")
    finally:
        connection.close()

def fetch_users_from_db():
    """Получает всех пользователей со статусом 0 из базы данных."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM users WHERE status = 0")
            users = cursor.fetchall()
            return [user['username'] for user in users]
    except pymysql.MySQLError as e:
        print(f"Ошибка при чтении пользователей из базы данных: {e}")
        return []
    finally:
        connection.close()

def update_user_status_in_db(username, new_status):
    """Обновляет статус пользователя в базе данных."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE users SET status = %s WHERE username = %s"
            cursor.execute(sql, (new_status, username))
            connection.commit()
            print(f"Статус пользователя {username} обновлен на {new_status}.")
    except pymysql.MySQLError as e:
        print(f"Ошибка при обновлении статуса пользователя {username}: {e}")
    finally:
        connection.close()
