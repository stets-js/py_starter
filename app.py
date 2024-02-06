# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import psycopg2

# Підключення до бази даних
conn = psycopg2.connect(
    dbname="etsscwgb",
    user="etsscwgb",
    password="5EPINOl1bzFmDxeLCZrOOws4C0-9Fb7A",
    host="snuffleupagus.db.elephantsql.com",
    port="5432"
)

# Створення курсора для виконання SQL запитів
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Привіт, світ! Це бекенд на Python і він працює!'

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data['username']
    password = data['password']

    # Виконання SQL запиту для додавання юзера в таблицю
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cur.execute(sql, (username, password))
    conn.commit()

    return jsonify({'message': 'User added successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
