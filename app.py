# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

# Підключення до бази даних
conn = psycopg2.connect(
    dbname="etsscwgb",
    user="etsscwgb",
    password="5EPINOl1bzFmDxeLCZrOOws4C0-9Fb7A",
    host="snuffleupagus.db.elephantsql.com",
    port="5432"
)

cur = conn.cursor()

app = Flask(__name__)
CORS(app, origind=['http://localhost:3000/'])

@app.route('/')
def index():
    return 'Привіт, світ! Це бекенд на Python і він працює!'


@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    user_list = []
    for user in users:
        user_data = {
            'id': user[0],
            'username': user[1],
            'password': user[2]
        }
        user_list.append(user_data)
    cur.close()
    return jsonify(user_list)

# Додати нового користувача
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data['username']
    password = data['password']

    # Перевірка наявності користувача в базі
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()
    if existing_user:
        cur.close()
        return jsonify({'error': 'User already exists'})

    # Додавання користувача, якщо його немає в базі
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cur.execute(sql, (username, password))
    conn.commit()
    cur.close()
    return jsonify({'message': 'User added successfully'})

# Отримати інформацію про користувача за логіном
@app.route('/get_user/<username>', methods=['GET'])
def get_user(username):
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_data = {
            'id': user[0],
            'username': user[1],
            'password': user[2]
        }
        cur.close()
        return jsonify(user_data)
    else:
        cur.close()
        return jsonify({'error': 'User not found'})

# Оновити інформацію про користувача за логіном
@app.route('/update_user/<username>', methods=['PUT'])
def update_user(username):
    data = request.json
    new_username = data['new_username']
    new_password = data['new_password']

    # Перевірка наявності користувача в базі
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()
    if not existing_user:
        cur.close()
        return jsonify({'error': 'User not found'})

    # Оновлення інформації про користувача, якщо він існує
    sql = "UPDATE users SET username = %s, password = %s WHERE username = %s"
    cur.execute(sql, (new_username, new_password, username))
    conn.commit()
    cur.close()
    return jsonify({'message': 'User updated successfully'})

# Видалити користувача за логіном
@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    # Перевірка наявності користувача в базі
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()
    if not existing_user:
        cur.close()
        return jsonify({'error': 'User not found'})

    # Видалення користувача, якщо він існує
    sql = "DELETE FROM users WHERE username = %s"
    cur.execute(sql, (username,))
    conn.commit()
    cur.close()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
