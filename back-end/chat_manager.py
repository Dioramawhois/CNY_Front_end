# chat_manager.py

from utils.logger import logger

class ChatManager:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    async def send_message(self, user_id, message):
        try:
            await self.telegram_client.send_message(user_id, message)
            logger.info(f"Message sent to {user_id}: {message}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {e}")
