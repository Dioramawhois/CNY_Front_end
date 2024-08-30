import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from utils.logger import logger

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logger.info("Database connection established")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        logger.info("Database connection closed")

    def add_user(self, user_id, username, first_name, date_added, user_type):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (userid, username, user_firstname, date_added, type) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, username, first_name, date_added, user_type)
                )
                self.connection.commit()
                logger.info(f"User {username} added to the database.")
        except Exception as e:
            logger.error(f"Error adding user {username} to the database: {e}")
            self.connection.rollback()

    def list_users(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            return []

    def delete_user(self, user_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE userid = %s", (user_id,))
                self.connection.commit()
                logger.info(f"User with ID {user_id} deleted from the database.")
        except Exception as e:
            logger.error(f"Error deleting user with ID {user_id}: {e}")
            self.connection.rollback()

    def is_user_in_whitelist(self, user_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM whitelist WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            logger.error(f"Error checking whitelist for user {user_id}: {e}")
            return False
