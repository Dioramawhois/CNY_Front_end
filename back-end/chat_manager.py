from telethon import TelegramClient

class ChatManager:
    def __init__(self, api_id, api_hash, bot_token):
        self.client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    async def send_message(self, user_id, message):
        try:
            await self.client.send_message(user_id, message)
            print(f"Message sent to user: {user_id}")
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    async def send_message_to_all(self, user_ids, message):
        for user_id in user_ids:
            await self.send_message(user_id, message)
