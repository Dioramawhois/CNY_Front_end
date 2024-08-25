# telegram_client.py

from telethon import TelegramClient
from config import API_ID, API_HASH

class TelegramClientWrapper:
    def __init__(self):
        self.client = TelegramClient('session_name', API_ID, API_HASH)

    async def start(self):
        await self.client.start()
        print("Telegram client started")

    async def get_entity(self, username):
        return await self.client.get_entity(username)

    async def send_message(self, user_id, message):
        await self.client.send_message(user_id, message)

    async def disconnect(self):
        await self.client.disconnect()

telegram_client = TelegramClientWrapper()
