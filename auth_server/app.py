import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'users.db')

app = Flask(__name__)
app.secret_key = os.environ.get('AUTH_APP_SECRET', 'dev-secret-change-me')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db()
        conn.execute(
            '''CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )'''
        )
        conn.commit()
        conn.close()


@app.before_first_request
def startup():
    init_db()


@app.route('/')
def index():
    if session.get('user'):
        return redirect(url_for('profile'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user'] = {'id': user['id'], 'email': user['email']}
            flash('Logged in successfully.', 'success')
            return redirect(url_for('profile'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        if not email or not password:
            flash('Email and password required.', 'warning')
            return render_template('register.html')
        if password != password2:
            flash('Passwords do not match.', 'warning')
            return render_template('register.html')
        hashed = generate_password_hash(password)
        try:
            conn = get_db()
            conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed))
            conn.commit()
            conn.close()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered.', 'warning')
    return render_template('register.html')


@app.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return f"<h3>Welcome, {user['email']}!</h3><p><a href='{url_for('logout')}'>Logout</a></p>"


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
