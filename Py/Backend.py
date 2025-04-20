import eventlet
eventlet.monkey_patch()

import subprocess
import sys
import time
import random
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import mysql.connector
import bcrypt

from MultiplayerGame import Game, BRICK_COLORS, Paddle, Ball, PowerUp
from settings        import *
from brick import Brick

# Install required packages if not already installed
def install_required_packages():
    required_packages = [
        'flask',
        'flask-socketio',
        'eventlet',
        'mysql-connector-python',
        'bcrypt',
        'python-socketio',
        'python-engineio'
    ]
    for pkg in required_packages:
        try:
            __import__(pkg.replace('-', '_'))
        except ImportError:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_required_packages()

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = b'xW\xc9\xc07}.ml\xe3\x10"8J\xd4\x13\x892V\x7f\x97c\xed\x06'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Database configuration
db_config = {
    'host':     'brickbreaker.cmtequ2gmttp.us-east-1.rds.amazonaws.com',
    'user':     'admin',
    'password': 'Brickbreaker',
    'database': 'brickBreaker'
}

# Store game rooms and their states
rooms_data = {}

# GameState class manages the state of each game room
class GameState:
    def __init__(self):
        self.game = Game(None)
        self.game.reset()
        self.game_started = False
        self.last_update   = time.time()
        print(f"Initialized GameState with {len(self.game.bricks)} bricks")

    # Update game state based on time elapsed
    def update(self):
        if self.game_started and not self.game.paused and not self.game.winner:
            now = time.time()
            dt  = now - self.last_update
            self.last_update = now
            self.game.update()
            if self.game.winner:
                self.game.powerups.clear()

    # Serialize game state for host player
    def serialize_for_host(self):
        bricks = [{
            'rect': {'x': b['rect'].x, 'y': b['rect'].y, 'width': b['rect'].width, 'height': b['rect'].height},
            'color': b['color'],
            'active': b['active']
        } for b in self.game.bricks]
        powerups = [{
            'rect': {'x': p.rect.x, 'y': p.rect.y, 'width': p.rect.width, 'height': p.rect.height},
            'type': p.type,
            'speed': p.speed,
            'color': p.color_map[p.type],
            'label': p.label_map[p.type]
        } for p in self.game.powerups]
        return {
            'host_paddle': {'x': self.game.player1.rect.x, 'y': self.game.player1.rect.y},
            'client_paddle': {'x': self.game.player2.rect.x, 'y': self.game.player2.rect.y},
            'host_ball': {
                'x': self.game.ball1.x, 'y': self.game.ball1.y,
                'vx': self.game.ball1.vx, 'vy': self.game.ball1.vy,
                'active': self.game.ball1.active
            },
            'client_ball': {
                'x': self.game.ball2.x, 'y': self.game.ball2.y,
                'vx': self.game.ball2.vx, 'vy': self.game.ball2.vy,
                'active': self.game.ball2.active
            },
            'host_lives': self.game.lives1,
            'client_lives': self.game.lives2,
            'host_score': self.game.player1.score,
            'client_score': self.game.player2.score,
            'bricks': bricks,
            'powerups': powerups,
            'game_started': self.game.game_started,
            'countdown': self.game.countdown,
            'paused': self.game.paused,
            'winner': self.game.winner
        }

    # Serialize game state for client player (swaps host/client data)
    def serialize_for_client(self):
        state = self.serialize_for_host()
        return {
            'host_paddle': state['client_paddle'],
            'client_paddle': state['host_paddle'],
            'host_ball': state['client_ball'],
            'client_ball': state['host_ball'],
            'host_lives': state['client_lives'],
            'client_lives': state['host_lives'],
            'host_score': state['client_score'],
            'client_score': state['host_score'],
            'bricks': state['bricks'],
            'powerups': state['powerups'],
            'game_started': state['game_started'],
            'countdown': state['countdown'],
            'paused': state['paused'],
            'winner': state['winner']
        }

# Main game loop for each room
def game_loop(room):
    gs = rooms_data[room]['game_state']
    host = rooms_data[room]['host_sid']
    client = rooms_data[room].get('client_sid')
    while gs.game_started and not gs.game.winner:
        gs.update()
        socketio.emit('game_state_update', gs.serialize_for_host(), room=host)
        if client:
            socketio.emit('game_state_update', gs.serialize_for_client(), room=client)
        socketio.sleep(1/60)

# HTTP routes for user authentication
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    uname, pwd = data['username'], data['password']
    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    try:
        conn = mysql.connector.connect(**db_config)
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO Users (username, password_hash) VALUES (%s,%s)",
            (uname, hashed)
        )
        conn.commit()
        return jsonify({"message": "User registered"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close(); conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    uname, pwd = data['username'], data['password']
    conn = mysql.connector.connect(**db_config)
    cur  = conn.cursor()
    cur.execute("SELECT user_id, password_hash FROM Users WHERE username=%s", (uname,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if row and bcrypt.checkpw(pwd.encode(), row[1].encode()):
        return jsonify({"message": "Login successful", "user_id": row[0]}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Socket.IO event handlers
@socketio.on('connect')
def on_connect():
    sid = request.sid
    print(f"[SERVER] Client connected: {sid}")
    emit('status', {'message':'Connected to server'})

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    print(f"[SERVER] Client disconnected: {sid}")
    for room, data in list(rooms_data.items()):
        if data['host_sid'] == sid:
            if 'client_sid' in data:
                emit('status', {'message':'Host left. Game ended.'}, room=data['client_sid'])
            del rooms_data[room]
            print(f"[SERVER] Room {room} cleared due to host disconnection")
        elif data.get('client_sid') == sid:
            data['client_sid'] = None
            data['client_username'] = None

@socketio.on('set_username')
def on_set_username(data):
    sid = request.sid
    username = data.get('username')
    for room, data in rooms_data.items():
        if data['host_sid'] == sid:
            data['host_username'] = username
            print(f"[SERVER] Host username set to {username} in room {room}")
        elif data.get('client_sid') == sid:
            data['client_username'] = username
            print(f"[SERVER] Client username set to {username} in room {room}")

@socketio.on('join_game')
def handle_join_game(data):
    sid = request.sid
    room = data.get('room')
    username = data.get('username')

    if room not in rooms_data:
        rooms_data[room] = {
            'host_sid': sid,
            'host_username': username,
            'game_state': GameState()
        }
        join_room(room)
        emit('set_as_host', {'room': room, 'host_username': username})
        print(f"[SERVER] Room {room} created by {username}")
    else:
        if rooms_data[room].get('client_sid') is None:
            rooms_data[room]['client_sid'] = sid
            rooms_data[room]['client_username'] = username
            join_room(room)
            emit('set_as_client', {'room': room, 'client_username': username})
            print(f"[SERVER] {username} joined room {room}")
        else:
            emit('status', {'message': 'Room is full'})

@socketio.on('ready')
def handle_ready(data):
    room = data.get('room')
    if room in rooms_data:
        if not rooms_data[room]['game_state'].game_started:
            rooms_data[room]['game_state'].game_started = True
            socketio.start_background_task(game_loop, room)
            print(f"[SERVER] Game started in room {room}")

@socketio.on('move')
def handle_move(data):
    room = data.get('room')
    x = data.get('x')
    if room in rooms_data:
        gs = rooms_data[room]['game_state']
        if request.sid == rooms_data[room]['host_sid']:
            gs.game.player1.rect.x = x
        elif request.sid == rooms_data[room].get('client_sid'):
            gs.game.player2.rect.x = x

@socketio.on('pause')
def handle_pause(data):
    room = data.get('room')
    if room in rooms_data:
        rooms_data[room]['game_state'].game.paused = not rooms_data[room]['game_state'].game.paused
        emit('paused', {'paused': rooms_data[room]['game_state'].game.paused}, room=room)

@socketio.on('restart')
def handle_restart(data):
    room = data.get('room')
    if room in rooms_data:
        gs = rooms_data[room]['game_state']
        gs.game.reset()
        gs.game_started = False
        emit('restarted', room=room)
        print(f"[SERVER] Game restarted in room {room}")

# Start the server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
