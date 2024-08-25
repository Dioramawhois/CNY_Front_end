# db_manager.py

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
        self.cursor = self.connection.cursor()
        logger.info("Database connection established")

    def add_user(self, user_id, username, first_name, date_added, user_type):
        try:
            self.cursor.execute(
                "INSERT INTO users (userid, username, user_firstname, date_added, type) VALUES (%s, %s, %s, %s, %s)",
                (user_id, username, first_name, date_added, user_type)
            )
            self.connection.commit()
            logger.info(f"User {username} added to the database.")
        except Exception as e:
            logger.error(f"Error adding user {username}: {e}")
            self.connection.rollback()

    def list_users(self):
        try:
            self.cursor.execute("SELECT * FROM users ORDER BY userid ASC")
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return []

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE userid = %s", (user_id,))
            self.connection.commit()
            logger.info(f"User {user_id} deleted from the database.")
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()
        logger.info("Database connection closed")
