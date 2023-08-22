from os import abort
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

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
