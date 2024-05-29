from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = []
tasks = []

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if any(user['username'] == data['username'] for user in users):
        return jsonify({"message": "User already exists"}), 400
    users.append(data)
    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = next((user for user in users if user['username'] == data['username'] and user['password'] == data['password']), None)
    if user:
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    tasks.append(data)
    return jsonify({"message": "Task added successfully"})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task.get('id') == task_id:
            task.update(data)
            return jsonify({"message": "Task updated successfully"})
    return jsonify({"message": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task.get('id') != task_id]
    return jsonify({"message": "Task deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
