# ==========================================================
#  © Pranshu2OP Production - Proprietary Code
#  All Rights Reserved.
#
#  This source code is the property of Pranshu2OP Production.
#  Unauthorized copying, modification, distribution, or use 
#  of this code is strictly prohibited.
#
#  For authorized access or licensing inquiries, contact:
#  pranshu2op@gmail.com
# ==========================================================

from flask import Flask, request, jsonify, render_template
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# Set the path for the SQLite database in the instance folder
db_path = os.path.join(app.instance_path, 'tododb.db')
os.makedirs(app.instance_path, exist_ok=True)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database
def initialize_db():
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            todo_name TEXT NOT NULL,
            description TEXT,
            start_time TEXT,
            due_date TEXT,
            priority TEXT
        )''')
        conn.commit()

initialize_db()



# Entry point for the frontend
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/index.html')
def indexhtml():
    return render_template('index.html')
@app.route('/login.html')
def login():
    return render_template('login.html')
@app.route('/setting.html')
def settiing():
    return render_template('setting.html')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# Add a new todo
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()

    # Validate and parse the due date in "YYYY-MM-DD HH:MM AM/PM" format
    try:
        due_date = datetime.strptime(data.get('due_date', ''), '%Y-%m-%d %I:%M %p')
    except ValueError:
        return jsonify({"error": "Invalid due date format. Please use YYYY-MM-DD HH:MM AM/PM."}), 400

    # Insert the new todo with the current date and time for start_time 
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO todos (todo_name, description, start_time, due_date, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('todo_name'),
            data.get('description'),
            datetime.now().strftime('%Y-%m-%d %I:%M %p'),
            due_date.strftime('%Y-%m-%d %I:%M %p'),
            data.get('priority')
        ))
        conn.commit()
    return jsonify({"message": "Todo added successfully!"}), 200

# View all todos
@app.route('/todos', methods=['GET'])
def view_todos():
    with get_db_connection() as conn:
        todos = conn.execute('SELECT * FROM todos').fetchall()
    return jsonify([dict(todo) for todo in todos]), 200

# Update a todo by ID
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()

    # Validate and parse the due date in "YYYY-MM-DD HH:MM AM/PM" format
    try:
        due_date = datetime.strptime(data.get('due_date', ''), '%Y-%m-%d %I:%M %p')
    except ValueError:
        return jsonify({"error": "Invalid due date format. Please use YYYY-MM-DD HH:MM AM/PM."}), 400

    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Todo ID not found."}), 404

        conn.execute('''
            UPDATE todos SET todo_name = ?, description = ?, due_date = ?, priority = ?
            WHERE id = ?
        ''', (
            data.get('todo_name'),
            data.get('description'),
            due_date.strftime('%Y-%m-%d %I:%M %p'),
            data.get('priority'),
            todo_id
        ))
        conn.commit()
    return jsonify({"message": "Todo updated successfully!"}), 200

# Delete a todo by ID
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if todo_id == 6:
        return jsonify({"error": "This Todo cannot be deleted as this is made by real engineer."}), 403
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Todo ID not found."}), 404

        conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
    return jsonify({"message": "Todo deleted successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
