import sys
import datetime as _dt
import threading
import pygame
import socketio

from network_config import SERVER_IP, SERVER_PORT
from client_utils   import transform_position
from settings       import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GAME_WIDTH,   GAME_HEIGHT,
    PADDLE_WIDTH, PADDLE_HEIGHT,
    BALL_RADIUS,  BRICK_WIDTH,  BRICK_HEIGHT,
    SCALE_FACTOR
)
from ui_constants   import BACKGROUND_COLOR, TEXT_COLOR
from MultiUi        import UIElement

# Game constants
PADDLE_SPEED = int(8 * SCALE_FACTOR)

# Power-up colors and labels
POWERUP_COLORS = {
    'slow_ball' : (241, 196,  15),
    'extra_life': ( 46, 204, 113)
}
POWERUP_LABELS = {
    'slow_ball' : 'S',
    'extra_life': '+'
}

# Logging helper function
def _log(message: str):
    ts = _dt.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[CLIENT {ts}] {message}")

# Initialize Socket.IO client and game state
sio          = socketio.Client()
local_id     = None
room         = None
usernames    = {'host': None, 'client': None}
latest_state = {}

# Game play area position
play_x = (SCREEN_WIDTH - GAME_WIDTH) // 2
play_y = (SCREEN_HEIGHT - GAME_HEIGHT) // 2

# Draw power-up on screen
def _draw_powerup(surface: pygame.Surface, pu_dict: dict):
    px, py = transform_position(pu_dict['x'], pu_dict['y'],
                                play_y, GAME_HEIGHT, local_id)
    rect = pygame.Rect(px, py, pu_dict['w'], pu_dict['h'])
    ptype = pu_dict['type']

    pygame.draw.ellipse(surface, POWERUP_COLORS[ptype], rect)

    font  = pygame.font.Font(None, 24)
    label = font.render(POWERUP_LABELS[ptype], True, (0, 0, 0))
    surface.blit(label, label.get_rect(center=rect.center))

# Socket.IO event handlers
@sio.event
def connect():
    _log("Connected to server")

@sio.event
def disconnect():
    _log("Disconnected from server")

@sio.on('set_as_host')
def on_set_as_host(data):
    global local_id, room
    local_id = 1
    room = data['room']
    usernames['host'] = data.get('host_username')
    _log(f"ROLE → HOST   | room = «{room}» | username = {usernames['host']}")

@sio.on('set_as_client')
def on_set_as_client(data):
    global local_id, room
    local_id = 2
    room = data['room']
    usernames['client'] = data.get('client_username')
    _log(f"ROLE → CLIENT | room = «{room}» | username = {usernames['client']}")

@sio.on('countdown')
def on_countdown(data):
    val = data['value']
    latest_state['countdown'] = val
    _log(f"COUNTDOWN = {val}")

    if val == "Go!":
        threading.Timer(1.0, lambda: latest_state.pop('countdown', None)).start()

@sio.on('game_state')
def on_game_state(data):
    bricks_total  = len(data.get('bricks', []))
    bricks_active = sum(b.get('active') for b in data.get('bricks', []))
    _log(f"GAME_STATE recv | bricks {bricks_active}/{bricks_total} active | "
         f"p1x={data['host_paddle']['x']} p2x={data['client_paddle']['x']}")
    latest_state.update(data)

@sio.on('paused')
def on_paused(data):
    latest_state['paused'] = data['paused']
    _log(f"PAUSED = {data['paused']}")

@sio.on('restarted')
def on_restarted():
    latest_state.clear()
    _log("Game restarted – state cleared")

# Main game loop
def client_main(room_name: str, username: str):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BrickBreaker Together (Online)")
    clock = pygame.time.Clock()
    ui    = UIElement(screen)

    try:
        sio.connect(f"http://{SERVER_IP}:{SERVER_PORT}",
                    transports=['websocket', 'polling'])
    except socketio.exceptions.ConnectionError:
        _log(f"❌  Unable to reach server at {SERVER_IP}:{SERVER_PORT}")
        return

    sio.emit('join_game', {'room': room_name, 'username': username})
    _log(f"JOIN_GAME → room «{room_name}», user «{username}»")

    while local_id is None:
        pygame.time.wait(50)

    sio.emit('ready', {'room': room})
    _log("READY sent")

    running = True
    while running:
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and latest_state.get('winner'):
                    sio.emit('restart', {'room': room})
                    _log("RESTART requested")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                sio.emit('ready', {'room': room})
                _log("READY (mouse click)")

        # Handle paddle movement
        keys  = pygame.key.get_pressed()
        left  = keys[pygame.K_LEFT]  or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        paddle_key = 'host_paddle' if local_id == 1 else 'client_paddle'
        cur_x      = latest_state.get(paddle_key, {}).get('x')

        if cur_x is not None and (left or right):
            new_x = cur_x + (-PADDLE_SPEED if left else PADDLE_SPEED)
            min_x = play_x
            max_x = play_x + GAME_WIDTH - PADDLE_WIDTH
            new_x = max(min_x, min(new_x, max_x))
            sio.emit('move', {'room': room, 'x': new_x})
            _log(f"MOVE x={new_x}")

        # Draw waiting screen if game hasn't started
        waiting = ('countdown' not in latest_state and
                   not latest_state.get('game_started', False) and
                   not latest_state.get('bricks'))
        if waiting:
            screen.fill(BACKGROUND_COLOR)
            msg = pygame.font.SysFont(None, 48).render(
                "Waiting for opponent…", True, TEXT_COLOR)
            screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH//2,
                                                  SCREEN_HEIGHT//2)))
            pygame.display.flip()
            continue

        # Draw game elements
        screen.fill(BACKGROUND_COLOR)
        ui.draw_ui_panels(latest_state)

        pygame.draw.rect(screen, (0, 0, 0),
                         (play_x, play_y, GAME_WIDTH, GAME_HEIGHT),
                         border_radius=12)

        # Draw bricks
        for b in latest_state.get('bricks', []):
            if not b.get('active'):
                continue
            bx, by = transform_position(b['x'], b['y'],
                                        play_y, GAME_HEIGHT, local_id)
            brick_rect = pygame.Rect(bx, by, BRICK_WIDTH, BRICK_HEIGHT)
            pygame.draw.rect(screen, b['color'], brick_rect, border_radius=4)
            inner = brick_rect.inflate(-10, -10)
            shade = tuple(max(c - 40, 0) for c in b['color'])
            pygame.draw.rect(screen, shade, inner, border_radius=2)

        # Draw power-ups
        for pu in latest_state.get('powerups', []):
            _draw_powerup(screen, pu)

        # Draw paddles and balls
        for paddle_key, ball_key, col in [
            ('host_paddle',   'host_ball',   (52, 152, 219)),
            ('client_paddle', 'client_ball', (231,  76,  60))
        ]:
            p = latest_state.get(paddle_key, {})
            b = latest_state.get(ball_key, {})
            px, py = transform_position(p.get('x', 0), p.get('y', 0),
                                        play_y, GAME_HEIGHT, local_id)
            bx, by = transform_position(b.get('x', 0), b.get('y', 0),
                                        play_y, GAME_HEIGHT, local_id)

            pygame.draw.rect(screen, col,
                             (px, py, PADDLE_WIDTH, PADDLE_HEIGHT),
                             border_radius=10)
            pygame.draw.circle(screen, col,
                               (int(bx), int(by)), BALL_RADIUS)

        # Draw UI elements
        if 'countdown' in latest_state:
            ui.draw_countdown(latest_state['countdown'])
        if latest_state.get('paused'):
            ui.draw_pause_menu()
        if latest_state.get('winner'):
            ui.draw_game_over(latest_state['winner'], local_id)

        pygame.display.flip()

    _log("Quitting Pygame")
    pygame.quit()
    sys.exit()
