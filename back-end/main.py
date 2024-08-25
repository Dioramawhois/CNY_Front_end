from flask import Flask, request, jsonify
from db_manager import Database
from user_manager import UserManager
from chat_manager import ChatManager
from telegram_client import telegram_client
from utils.logger import logger
import asyncio

app = Flask(__name__)

db = Database()
user_manager = UserManager(telegram_client)
chat_manager = ChatManager(telegram_client)

# Глобальный event loop
loop = asyncio.get_event_loop()

@app.route('/api/users/add', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        logger.debug(data)
        
        identifiers = data.get('users', [])
        
        if isinstance(identifiers, str):
            identifiers = identifiers.split()
        
        logger.debug(identifiers)

        # Используем глобальный event loop
        for identifier in identifiers:
            if identifier.startswith('https://t.me/'):
                identifier = identifier.split('/')[-1]
            elif identifier.startswith('@'):
                pass
            else:
                try:
                    identifier = int(identifier)
                except ValueError:
                    logger.error(f"Invalid identifier format: {identifier}")
                    continue

            # Используем глобальный event loop для вызова асинхронной функции
            result = loop.run_until_complete(user_manager.add_user(db, identifier))
            logger.debug(f"User added: {result}")
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/users/list', methods=['GET'])
def list_users():
    try:
        users = user_manager.list_users(db)
        return jsonify(users), 200
    except Exception as e:
        logger.exception(f"Exception occurred while fetching users: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500

@app.route('/api/users/delete', methods=['POST'])
def delete_user():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        user_manager.delete_user(db, user_id)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.exception(f"Exception occurred while deleting user: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500
    
@app.route('/api/users/delete-all', methods=['POST'])
def delete_all_users():
    try:
        # Здесь можно добавить логику для удаления всех пользователей
        db.cursor.execute("DELETE FROM users")
        db.connection.commit()
        logger.info("All users deleted from the database.")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.exception(f"Exception occurred while deleting all users: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500


if __name__ == '__main__':
    # Инициализация Telegram клиента в глобальном event loop
    loop.run_until_complete(telegram_client.start())
    app.run(host='0.0.0.0', port=5000)
