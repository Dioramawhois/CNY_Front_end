import re

class UserManager:
    def __init__(self, database):
        self.db = database

    def add_users(self, input_data):
        users = self.parse_input(input_data)
        for user in users:
            self.db.add_user(user['user_id'], user['username'], user['user_firstname'])

    def delete_user(self, user_id):
        self.db.delete_user(user_id)

    def fetch_users(self):
        return self.db.fetch_users()

    def parse_input(self, input_data):
        users = []
        lines = input_data.splitlines()
        for line in lines:
            if line.isdigit():
                users.append({'user_id': line, 'username': None, 'user_firstname': None})
            elif line.startswith('https://t.me/'):
                username = line.split('/')[-1]
                users.append({'user_id': None, 'username': username, 'user_firstname': None})
            elif line.startswith('@'):
                username = line[1:]
                users.append({'user_id': None, 'username': username, 'user_firstname': None})
        return users
