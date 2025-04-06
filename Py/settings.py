# settings.py
import pygame

# Default values, updated after pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCALE_FACTOR = 1.0

# UI dimensions, updated after screen info is retrieved
UI_WIDTH = int(SCREEN_WIDTH * 0.15)
GAME_WIDTH = int(SCREEN_WIDTH * 0.65)
GAME_HEIGHT = int(SCREEN_HEIGHT * 0.75)

# Colors
PRIMARY_COLOR = (52, 152, 219)
BACKGROUND_COLOR = (0, 0, 0)
LIFE_COLOR = (231, 76, 60)

# Paddle settings
PADDLE_WIDTH = int(200 * SCALE_FACTOR)
PADDLE_HEIGHT = int(10 * SCALE_FACTOR)
PADDLE_Y = int(SCREEN_HEIGHT - 70 * SCALE_FACTOR)

# Ball settings
BALL_RADIUS = int(8 * SCALE_FACTOR)
BALL_SPEED = int(5 * SCALE_FACTOR)

# Brick settings
ROWS, COLS = 10, 20
BRICK_WIDTH = int(54 * SCALE_FACTOR)
BRICK_HEIGHT = int(20 * SCALE_FACTOR)
BRICK_PADDING = int(8 * SCALE_FACTOR)

# Font sizes
TITLE_FONT_SIZE = int(62 * SCALE_FACTOR)
LABEL_FONT_SIZE = int(40 * SCALE_FACTOR)
SCORE_FONT_SIZE = int(50 * SCALE_FACTOR)
SMALL_FONT_SIZE = int(32 * SCALE_FACTOR)
COUNTDOWN_FONT_SIZE = int(150 * SCALE_FACTOR)

def init_screen_dimensions():
    """Initialize screen dimensions after pygame.init() is called"""
    global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_FACTOR
    global UI_WIDTH, GAME_WIDTH, GAME_HEIGHT
    global PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_Y
    global BALL_RADIUS, BALL_SPEED
    global BRICK_WIDTH, BRICK_HEIGHT, BRICK_PADDING
    global TITLE_FONT_SIZE, LABEL_FONT_SIZE, SCORE_FONT_SIZE, SMALL_FONT_SIZE, COUNTDOWN_FONT_SIZE
    
    # Get screen info for fullscreen
    screen_info = pygame.display.Info()
    SCREEN_WIDTH = screen_info.current_w
    SCREEN_HEIGHT = screen_info.current_h
    
    # Calculate scaling factor based on screen size
    SCALE_FACTOR = min(SCREEN_WIDTH / 1920, SCREEN_HEIGHT / 1080)
    
    # Update UI dimensions
    UI_WIDTH = int(SCREEN_WIDTH * 0.15)
    GAME_WIDTH = int(SCREEN_WIDTH * 0.65)
    GAME_HEIGHT = int(SCREEN_HEIGHT * 0.75)
    
    # Update game element dimensions
    PADDLE_WIDTH = int(200 * SCALE_FACTOR)
    PADDLE_HEIGHT = int(10 * SCALE_FACTOR)
    PADDLE_Y = int(SCREEN_HEIGHT - 70 * SCALE_FACTOR)
    
    BALL_RADIUS = int(8 * SCALE_FACTOR)
    BALL_SPEED = int(5 * SCALE_FACTOR)
    
    BRICK_WIDTH = int(54 * SCALE_FACTOR)
    BRICK_HEIGHT = int(20 * SCALE_FACTOR)
    BRICK_PADDING = int(8 * SCALE_FACTOR)
    
    # Update font sizes
    TITLE_FONT_SIZE = int(62 * SCALE_FACTOR)
    LABEL_FONT_SIZE = int(40 * SCALE_FACTOR)
    SCORE_FONT_SIZE = int(50 * SCALE_FACTOR)
    SMALL_FONT_SIZE = int(32 * SCALE_FACTOR)
    COUNTDOWN_FONT_SIZE = int(150 * SCALE_FACTOR)
