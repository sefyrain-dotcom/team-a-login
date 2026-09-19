from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)

DATABASE = "accounts.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = hashlib.sha256(
        request.form["password"].encode()
    ).hexdigest()

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, password)
    ).fetchone()
    conn.close()

    if user:
        return f"<h1>Welcome, {user['name']}!</h1><p>Login successful.</p>"
    else:
        return "<h2>Invalid email or password</h2><a href='/'>Go Back</a>"

@app.route("/")
def home():
    return "<h1>TEAM A is working!</h1><p>Flask deployment successful.</p>"
    
@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    email = request.form["email"]
    password = hashlib.sha256(
        request.form["password"].encode()
    ).hexdigest()

    conn = get_db()

    try:
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        message = "Account created successfully!"
    except sqlite3.IntegrityError:
        message = "Email already exists!"

    conn.close()

    return f"<h2>{message}</h2><a href='/'>Go to Login</a>"


if __name__ == "__main__":
    app.run(debug=True)
