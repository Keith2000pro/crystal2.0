import sqlite3

def read_users_from_file(file_path):
    """Reads users from a text file and returns them as a set."""
    try:
        with open(file_path, 'r') as file:
            users = {line.strip() for line in file if line.strip()}  # Strip whitespace and ignore empty lines
        return users
    except Exception as e:
        print(f"Error reading from file {file_path}: {e}")
        return set()

def write_users_to_db(db_path, users):
    """Writes users to the database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE)")  # Set username as UNIQUE

        for username in users:
            cursor.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))
            print(f"User {username} written to database.")

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error writing to database {db_path}: {e}")

def main():
    file_path = 'users.txt'  # Path to your users.txt file
    db_path = 'users.sqlite3'  # SQLite database path

    users = read_users_from_file(file_path)  # Read users from file
    write_users_to_db(db_path, users)  # Write users to database

if __name__ == "__main__":
    main()
