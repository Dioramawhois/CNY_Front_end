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

# Флаг для отправки сообщений
is_sending_messages = False

def run_in_loop(coroutine):
    """
    Запускает корутину в существующем event loop.
    """
    return asyncio.run_coroutine_threadsafe(coroutine, loop)

@app.route('/api/start', methods=['POST'])
def start_sending_messages():
    global is_sending_messages
    try:
        data = request.get_json()
        message = data.get('message', '')
        if not message:
            return jsonify({"status": "failed", "error": "Message cannot be empty."}), 400
        
        is_sending_messages = True
        logger.info("Started sending messages to all users.")

        # Запускаем асинхронную отправку сообщений
        run_in_loop(send_messages_to_all_users(message))
        return jsonify({"status": "success", "echo": message}), 200
    except Exception as e:
        logger.error(f"Error starting message sending: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500

async def send_messages_to_all_users(message):
    """
    Асинхронная функция для отправки сообщений всем пользователям.
    """
    global is_sending_messages
    try:
        users = user_manager.list_users(db)
        for user in users:
            if not is_sending_messages:
                break
            identifier = user[1] if user[1] else user[0]  # Используем username, если он доступен, иначе user_id
            await chat_manager.send_message(identifier, message)
            logger.info(f"Message sent to user {identifier}")
    except Exception as e:
        logger.error(f"Error sending messages: {e}")

@app.route('/api/stop', methods=['POST'])
def stop_sending_messages():
    global is_sending_messages
    try:
        is_sending_messages = False
        logger.info("Stopped sending messages to all users.")
        return jsonify({"status": "success", "message": "Message sending stopped."}), 200
    except Exception as e:
        logger.error(f"Error stopping message sending: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500

@app.route('/api/users/add', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        logger.debug(data)
        
        identifiers = data.get('users', [])
        
        if isinstance(identifiers, str):
            identifiers = identifiers.split()
        
        logger.debug(identifiers)
        
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

            # Используем run_in_loop для запуска асинхронной функции
            future = run_in_loop(user_manager.add_user(db, identifier))
            result = future.result()
            logger.debug(f"User added: {result}")
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
        
@app.route('/api/users/list', methods=['GET'])
def list_users():
    try:
        users = user_manager.list_users(db)
        user_list = [{"userid": user[0], "username": user[1], "first_name": user[2], "type": user[4]} for user in users]
        return jsonify(user_list), 200
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
        db.cursor.execute("DELETE FROM users")
        db.connection.commit()
        logger.info("All users deleted from the database.")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.exception(f"Exception occurred while deleting all users: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == '__main__':
    # Инициализация Telegram клиента в глобальном event loop
    run_in_loop(telegram_client.start())
    app.run(host='0.0.0.0', port=5000)
