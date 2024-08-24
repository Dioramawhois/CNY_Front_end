from telethon.sync import TelegramClient
from telethon.errors import UsernameInvalidError
from config import API_ID, API_HASH

class UserManager:
    def __init__(self):
        self.client = TelegramClient('session_name', API_ID, API_HASH)
        self.client.start()

    def get_user_id(self, username):
        try:
            user = self.client.get_entity(username)
            return user.id, user.username, user.first_name
        except UsernameInvalidError:
            return None

    def add_user(self, db, username):
        user_info = self.get_user_id(username)
        if user_info:
            user_id, username, user_firstname = user_info
            db.add_user(user_id, username, user_firstname, '2024-08-24', 'user')
            return True
        else:
            return False
