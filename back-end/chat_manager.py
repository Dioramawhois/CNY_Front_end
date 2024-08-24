from telethon.sync import TelegramClient
from config import API_ID, API_HASH

class ChatManager:
    def __init__(self):
        self.client = TelegramClient('session_name', API_ID, API_HASH)
        self.client.start()

    def send_message(self, user_id, message):
        self.client.send_message(user_id, message)

    def broadcast(self, db, message):
        users = db.get_all_users()
        for user in users:
            self.send_message(user[0], message)
