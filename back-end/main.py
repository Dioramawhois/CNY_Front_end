from flask import Flask, request, jsonify
from user_manager import UserManager
from chat_manager import ChatManager
from db_manager import Database

app = Flask(__name__)
db = Database()
user_manager = UserManager()
chat_manager = ChatManager()

@app.route('/api/users/add', methods=['POST'])
def add_user():
    username = request.json.get('username')
    if user_manager.add_user(db, username):
        return jsonify({"status": "success", "message": f"User {username} added successfully"}), 200
    else:
        return jsonify({"status": "error", "message": f"Could not add user: {username}"}), 400

@app.route('/api/users/delete', methods=['POST'])
def delete_user():
    user_id = request.json.get('user_id')
    db.delete_user(user_id)
    return jsonify({"status": "success", "message": f"User {user_id} deleted successfully"}), 200

@app.route('/api/users/list', methods=['GET'])
def list_users():
    users = db.get_all_users()
    return jsonify(users), 200

@app.route('/api/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')
    chat_manager.broadcast(db, message)
    return jsonify({"status": "success", "message": "Message broadcasted successfully"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
