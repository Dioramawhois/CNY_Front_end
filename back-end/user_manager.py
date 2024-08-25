# user_manager.py

from utils.logger import logger
from telethon.errors import UsernameInvalidError, UserNotMutualContactError, ChannelPrivateError, ChannelInvalidError
from telethon.tl.types import User, Channel  # Добавьте этот импорт
from datetime import datetime

class UserManager:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    async def add_user(self, db, identifier):
        try:
            logger.debug('Work 1\n')
            # Получаем объект пользователя или чата
            user = await self.telegram_client.get_entity(identifier)
            logger.debug(f'{user}\n')
            
            user_id = user.id
            username = user.username or "N/A"
            first_name = user.first_name or "N/A"

            # Определяем тип пользователя
            if isinstance(user, User):
                user_type = "User" if not user.bot else "Bot"
            elif isinstance(user, Channel):
                user_type = "Channel"
            else:
                user_type = "Chat"
            date_added = datetime.now()

            db.add_user(user_id, username, first_name, date_added, user_type)
            logger.info(f"User {username} added successfully.")
            return True
        except (UsernameInvalidError, UserNotMutualContactError, ChannelPrivateError, ChannelInvalidError) as e:
            logger.error(f"Error adding user {identifier}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error adding user {identifier}: {e}")
            return False


    def list_users(self, db):
        return db.list_users()

    def delete_user(self, db, user_id):
        return db.delete_user(user_id)
