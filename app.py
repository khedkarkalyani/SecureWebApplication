from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_bcrypt import Bcrypt
from config import Config 

app = Flask(__name__)
app.config.from_object(Config)
app.config['GITHUB_CLIENT_ID'] = "Ov23liytuNLdouTLoGrA"
app.config['GITHUB_CLIENT_SECRET'] = "5c8141a6f5bab6969c5ad4094bf32b1eefc94942"
bcrypt = Bcrypt(app)

# -----------------------------
# Create Database (if not exists)
# -----------------------------
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Home Route
# -----------------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# -----------------------------
# Register Route
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# -----------------------------
# Login Route
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[3], password):
            return render_template('dashboard.html')
        else:
            return "Invalid Credentials!"

    return render_template('login.html')

# -----------------------------
# Dashboard Route
# -----------------------------
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('<a href="/logout">Logout</a>')
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
