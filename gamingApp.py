from flask import Flask, redirect, render_template, request, url_for, flash
import sqlite3, secrets
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = secrets.token_hex(16)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, email, password, platform):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.platform = platform

@login_manager.user_loader
def load_user(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data['id'], user_data['username'], user_data['email'], user_data['password'], user_data['platform'])
        return None

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
        
    user = User(cursor.lastrowid, username, email, hashed_password, platform)
    login_user(user)

    conn.commit()
    conn.close()

    flash('Your account has been created!', 'success')

    return redirect(url_for('newProfile', username=username, platform=platform))


@app.route('/newProfile/<username>/<platform>')
def newProfile(username, platform):
    return render_template('newProfile.html', username=username, platform=platform)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                stored_password = user_data['password']
                if bcrypt.check_password_hash(stored_password, password):
                    # Login successful
                    user = User(user_data['id'], user_data['username'], user_data['email'], stored_password, user_data['platform'])
                    login_user(user)
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('profile'))
                else:
                    flash('Login failed. Please check your credentials.', 'error')
            else:
                flash('User not found. Please register.', 'error')

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

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash('Logged out successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
