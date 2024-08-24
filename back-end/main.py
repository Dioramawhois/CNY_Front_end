from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from database import Database
from chat_manager import ChatManager
from user_manager import UserManager

app = Flask(__name__)
CORS(app)

# Настройки базы данных и Telegram
db = Database(host="localhost", database="telegram", user="bot", password="VPS")
chat_manager = ChatManager(api_id='YOUR_API_ID', api_hash='YOUR_API_HASH', bot_token='YOUR_BOT_TOKEN')
user_manager = UserManager(db)

# Логика рассылки
is_sending = False

@app.route('/api/start', methods=['POST'])
def start_sending():
    global is_sending
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "Message is required"}), 400

    is_sending = True
    asyncio.run(send_message_to_all_users(message))
    
    return jsonify({"status": "started", "echo": message})

@app.route('/api/stop', methods=['POST'])
def stop_sending():
    global is_sending
    is_sending = False
    return jsonify({"status": "stopped"})

async def send_message_to_all_users(message):
    global is_sending
    users = user_manager.fetch_users()
    user_ids = [user[0] for user in users]

    if is_sending:
        await chat_manager.send_message_to_all(user_ids, message)

@app.route('/api/users/add', methods=['POST'])
def add_user():
    data = request.json
    user_manager.add_users(data.get('users', ''))
    return jsonify({"status": "Users added"})

@app.route('/api/users/delete', methods=['POST'])
def delete_user():
    data = request.json
    user_id = data.get('user_id')
    user_manager.delete_user(user_id)
    return jsonify({"status": "User deleted"})

@app.route('/api/users/list', methods=['GET'])
def list_users():
    users = user_manager.fetch_users()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
