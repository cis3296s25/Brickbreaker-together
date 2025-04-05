import mysql.connector
import hashlib

def connect_db():
    return mysql.connector.connect(
        host='brickbreaker.cmtequ2gmttp.us-east-1.rds.amazonaws.com',
        user='admin',
        password='Brickbreaker',
        database='brickBreaker'
    )

# User Accounts

def get_user_by_username(username):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT user_id, username, password_hash FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def create_user(username, password):
    # Using SHA-256 for password hashing
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed_pw))
    conn.commit()
    cursor.close()
    conn.close()

# ---------- High Scores ----------

def update_high_score(user_id, score):
    """
    Insert a new score or update an existing high score if the new score is greater.
    Assumes a table "scores" with columns: score_id, user_id, score, updated_at.
    """
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT score FROM scores WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    if row:
        # Update if new score is higher
        if score > row[0]:
            update_query = "UPDATE scores SET score = %s, updated_at = NOW() WHERE user_id = %s"
            cursor.execute(update_query, (score, user_id))
    else:
        # Insert new score record
        insert_query = "INSERT INTO scores (user_id, score, updated_at) VALUES (%s, %s, NOW())"
        cursor.execute(insert_query, (user_id, score))
    conn.commit()
    cursor.close()
    conn.close()

def get_high_score(user_id):
    """
    Retrieve the high score for a given user.
    Returns the score if available, otherwise None.
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT score FROM scores WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row['score'] if row else None

# Friend Relationships

def add_friend(user_id1, user_id2):
    """
    Add a friendship between two users.
    The pair (user_id1, user_id2) is stored uniquely. We can order the IDs to avoid duplicates.
    Assumes a table "user_friends" with columns: user_id1, user_id2, created_at.
    """
    conn = connect_db()
    cursor = conn.cursor()
    # Order the user IDs (lowest first)
    u1, u2 = sorted([user_id1, user_id2])
    query = "INSERT INTO user_friends (user_id1, user_id2, created_at) VALUES (%s, %s, NOW())"
    try:
        cursor.execute(query, (u1, u2))
        conn.commit()
    except mysql.connector.Error as err:
        # Optionally, handle error (e.g., duplicate friendship)
        print("Error adding friend:", err)
    cursor.close()
    conn.close()

def get_friends(user_id):
    """
    Retrieve a list of friend user IDs for a given user.
    Checks both columns of the user_friends table.
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT 
        CASE 
            WHEN user_id1 = %s THEN user_id2
            ELSE user_id1
        END AS friend_id
    FROM user_friends
    WHERE user_id1 = %s OR user_id2 = %s
    """
    cursor.execute(query, (user_id, user_id, user_id))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row['friend_id'] for row in rows]

# Multiplayer Sessions

def create_session(session_name):
    """
    Create a new game session.
    Assumes a table "sessions" with columns: session_id (auto-increment), session_name, created_at.
    """
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO sessions (session_name, created_at) VALUES (%s, NOW())"
    cursor.execute(query, (session_name,))
    conn.commit()
    session_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return session_id

def get_session(session_id):
    """
    Retrieve details for a specific game session.
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT session_id, session_name, created_at FROM sessions WHERE session_id = %s"
    cursor.execute(query, (session_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

# ---------- Session Participants ----------

def add_session_participant(session_id, user_id):
    """
    Add a user to a game session.
    Assumes a table "session_participants" with columns: session_id, user_id, joined_at.
    """
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO session_participants (session_id, user_id, joined_at) VALUES (%s, %s, NOW())"
    cursor.execute(query, (session_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_session_participants(session_id):
    """
    Retrieve a list of user IDs participating in a given session.
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT user_id FROM session_participants WHERE session_id = %s"
    cursor.execute(query, (session_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row['user_id'] for row in rows]