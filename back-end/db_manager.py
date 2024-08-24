import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

class Database:
    def __init__(self):
        # Подключение к базе данных PostgreSQL
        self.connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def add_user(self, user_id, username, user_firstname, date_added, user_type):
        self.cursor.execute(
            "INSERT INTO users (userid, username, user_firstname, date_added, type) VALUES (%s, %s, %s, %s, %s)",
            (user_id, username, user_firstname, date_added, user_type)
        )
        self.connection.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE userid = %s", (user_id,))
        self.connection.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users ORDER BY userid ASC")
        return self.cursor.fetchall()
