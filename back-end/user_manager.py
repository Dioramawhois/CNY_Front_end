# user_manager.py

from utils.logger import logger
from telethon.errors import (
    UsernameInvalidError, UserNotMutualContactError,
    ChannelPrivateError, ChannelInvalidError
)
from datetime import datetime

class UserManager:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    async def add_user(self, db, identifier):
        try:
            logger.debug('Work 1\n')

            # Получаем объект пользователя или чата
            entity = await self.telegram_client.get_entity(identifier)
            logger.debug(entity)

            if hasattr(entity, 'first_name'):
                # Это пользователь
                user_id = entity.id
                username = entity.username or "N/A"
                first_name = entity.first_name or "N/A"
                user_type = "User"
            else:
                # Это чат
                user_id = entity.id
                username = entity.username or "N/A"
                first_name = entity.title or "N/A"  # Используем title вместо first_name
                user_type = "Chat"

            db.add_user(user_id, username, first_name, datetime.now(), user_type)
            logger.info(f"{user_type} {username} added successfully.")
            return True

        except (UsernameInvalidError, UserNotMutualContactError, ChannelPrivateError, ChannelInvalidError) as e:
            logger.error(f"Error adding {identifier}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error adding {identifier}: {e}")
            return False

    def list_users(self, db):
        return db.list_users()

    def delete_user(self, db, user_id):
        return db.delete_user(user_id)
