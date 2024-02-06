# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://etsscwgb:5EPINOl1bzFmDxeLCZrOOws4C0-9Fb7A@snuffleupagus.db.elephantsql.com/etsscwgb'
db = SQLAlchemy(app)

# Модель користувача
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Створення таблиць у базі даних
db.create_all()

# Реєстрація маршруту для логіну
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Успішний вхід
            flash('Успішний вхід!', 'success')
            return redirect(url_for('index'))
        else:
            # Невірний логін або пароль
            flash('Невірний логін або пароль. Спробуйте ще раз.', 'error')
    return render_template('login.html')

# Реєстрація маршруту за замовчуванням
@app.route('/')
def index():
    return 'Привіт, світ! Це мій перший бекенд на Python з Flask і він працює!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
