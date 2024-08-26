from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from db_manager import Database
from user_manager import UserManager
from chat_manager import ChatManager
from telegram_client import telegram_client
from utils.logger import logger
import asyncio
from threading import Thread
from telegram_bot import start_bot
import random
from config import Sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = '7c3bc7c74dfdd7921f29730ecaa5effc09f5b9b013a9ecf6'

# Настройка CORS для вашего приложения Flask
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")  # Разрешаем все источники

db = Database()
user_manager = UserManager(telegram_client)
chat_manager = ChatManager(telegram_client)

is_sending_messages = False  # Глобальная переменная для управления состоянием

# Создаем новый event loop в отдельном потоке
asyncio_loop = asyncio.new_event_loop()

def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Запускаем новый поток с event loop для asyncio
asyncio_thread = Thread(target=start_asyncio_loop, args=(asyncio_loop,))
asyncio_thread.start()

async def start_telegram_client():
    try:
        await telegram_client.start()
        logger.info("Telegram client started successfully.")
    except Exception as e:
        logger.error(f"Error starting Telegram client: {e}")

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

        # Используем run_coroutine_threadsafe для запуска корутины в новом event loop
        asyncio.run_coroutine_threadsafe(send_messages_to_all_users(message), asyncio_loop)

        return jsonify({"status": "success", "echo": message}), 200
    except Exception as e:
        logger.error(f"Error starting message sending: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500

async def send_messages_to_all_users(message):
    global is_sending_messages
    try:
        users = user_manager.list_users(db)
        logger.info(f"Sending messages to {len(users)} users.")
        for user in users:
            if not is_sending_messages:
                logger.info("Sending messages stopped.")
                break
            identifier = user[1] if user[1] else user[0]
            try:
                await chat_manager.send_message(identifier, message)
                random_sleep = random.randint(Sleep[0], Sleep[1])
                logger.debug(f'Ожидание {random_sleep} секунд перед отправкой следующего сообщения...')
                await asyncio.sleep(random_sleep)
                logger.info(f"Message sent to user {identifier}")

                # Отправляем лог в реальном времени через WebSocket всем клиентам
                socketio.emit('log', {'message': f"Message sent to user {identifier}"})
            except Exception as e:
                logger.error(f"Failed to send message to {identifier}: {e}")
                socketio.emit('log', {'message': f"Failed to send message to {identifier}: {e}"})
    except Exception as e:
        logger.error(f"Error sending messages: {e}")
        socketio.emit('log', {'message': f"Error sending messages: {e}"})

@app.route('/api/stop', methods=['POST'])
def stop_sending_messages():
    global is_sending_messages
    try:
        is_sending_messages = False
        logger.info("Stopped sending messages to all users.")
        socketio.emit('log', {'message': "Stopped sending messages to all users."})
        return jsonify({"status": "success", "message": "Message sending stopped."}), 200
    except Exception as e:
        logger.error(f"Error stopping message sending: {e}")
        socketio.emit('log', {'message': f"Error stopping message sending: {e}"})
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

            # Используем run_coroutine_threadsafe для вызова асинхронной функции
            future = asyncio.run_coroutine_threadsafe(user_manager.add_user(db, identifier), asyncio_loop)
            result = future.result()
            logger.debug(f"User added: {result}")
            socketio.emit('log', {'message': f"User {identifier} added: {result}"})
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        socketio.emit('log', {'message': f"Unexpected error: {e}"})
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
        socketio.emit('log', {'message': f"User {user_id} deleted."})
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.exception(f"Exception occurred while deleting user: {e}")
        socketio.emit('log', {'message': f"Error deleting user {user_id}: {e}"})
        return jsonify({"status": "failed", "error": str(e)}), 500

@app.route('/api/users/delete-all', methods=['POST'])
def delete_all_users():
    try:
        db.cursor.execute("DELETE FROM users")
        db.connection.commit()
        logger.info("All users deleted from the database.")
        socketio.emit('log', {'message': "All users deleted from the database."})
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.exception(f"Exception occurred while deleting all users: {e}")
        socketio.emit('log', {'message': f"Error deleting all users: {e}"})
        return jsonify({"status": "failed", "error": str(e)}), 500

@app.route('/api/check-whitelist', methods=['GET'])
def check_whitelist():
    try:
        user_id = request.args.get('user_id')
        logger.info(f"Checking whitelist for user_id: {user_id}")

        if user_id is None:
            return jsonify({"status": "failed", "error": "No user_id provided"}), 400

        # Используем готовый метод из db_manager.py
        is_authorized = db.is_user_in_whitelist(user_id)

        if is_authorized:
            logger.info(f"User {user_id} is authorized.")
            return jsonify({"status": "success", "authorized": True}), 200
        else:
            logger.info(f"User {user_id} is not authorized.")
            return jsonify({"status": "success", "authorized": False}), 200

    except Exception as e:
        logger.error(f"Error checking whitelist for user {user_id}: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == '__main__':
    # Запускаем телеграмм бота в отдельном потоке
    bot_thread = Thread(target=start_bot)
    bot_thread.start()

    # Запускаем Telegram клиент в новом event loop
    asyncio.run_coroutine_threadsafe(start_telegram_client(), asyncio_loop)
    socketio.run(app, host='0.0.0.0', port=5000)