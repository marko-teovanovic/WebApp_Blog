from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__)

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
                        password TEXT NOT NULL
                    )''')

    conn.commit()
    conn.close()

create_table()

@app.route('/register', methods=['POST'])
def save_profile():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (username, email, password))

    conn.commit()
    conn.close()

    return redirect(url_for('profile', username=username)) 

@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/consoles')
def consoles():
    return render_template('consoles.html')

@app.route('/newReleases')
def newReleases():
    return render_template('newReleases.html')

if __name__ == '__main__':
    app.run(debug=True)
