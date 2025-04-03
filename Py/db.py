import mysql.connector
import hashlib

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='G0p@!2025',
        database='brickbreaker'
    )

def get_user_by_username(username):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT user_id, username, password_hash FROM users WHERE username=%s"
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def create_user(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed_pw))
    conn.commit()
    cursor.close()
    conn.close()