from flask import Flask, redirect, render_template, request, url_for, flash
import sqlite3, secrets
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = secrets.token_hex(16)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        platform TEXT NOT NULL
                    )''')

    conn.commit()
    conn.close()

create_table()

from flask import flash

@app.route('/register', methods=['POST'])
def save_profile():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']
    platform = request.form.get('platform')

    if password != confirm_password:
        flash('Password and confirm password do not match.', 'error')
        return redirect(url_for('register'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password, platform) VALUES (?, ?, ?, ?)",
                    (username, email, hashed_password, platform))
    conn.commit()
    conn.close()

    flash('Your account has been created!', 'success')

    return redirect(url_for('newProfile', username=username, platform=platform))


@app.route('/newProfile/<username>/<platform>')
def newProfile(username, platform):
    return render_template('newProfile.html', username=username, platform=platform)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/pc')
def pc():
    return render_template('pc.html')

@app.route('/xbox')
def xbox():
    return render_template('xbox.html')

@app.route('/playStation')
def playStation():
    return render_template('playStation.html')

@app.route('/nintendo')
def nintendo():
    return render_template('nintendo.html')

@app.route('/newReleases')
def newReleases():
    return render_template('newReleases.html')

if __name__ == '__main__':
    app.run(debug=True)
