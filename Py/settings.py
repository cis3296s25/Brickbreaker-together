# settings.py
import pygame

# Constant screen dimensions
SCREEN_WIDTH = 1440 #1440 #1920 #1080
SCREEN_HEIGHT = 900 #900 #1080  
SCALE_FACTOR = 1.0

# UI dimensions (constant)
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
LABEL_FONT_SIZE = int(32 * SCALE_FACTOR)
SCORE_FONT_SIZE = int(50 * SCALE_FACTOR)
SMALL_FONT_SIZE = int(28 * SCALE_FACTOR)
COUNTDOWN_FONT_SIZE = int(150 * SCALE_FACTOR)

def init_screen_dimensions():
    """Initialize screen dimensions based on current SCREEN_WIDTH and SCREEN_HEIGHT"""
    global UI_WIDTH, GAME_WIDTH, GAME_HEIGHT, SCALE_FACTOR
    global PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_Y
    global BALL_RADIUS, BALL_SPEED
    global BRICK_WIDTH, BRICK_HEIGHT, BRICK_PADDING
    global TITLE_FONT_SIZE, LABEL_FONT_SIZE, SCORE_FONT_SIZE, SMALL_FONT_SIZE, COUNTDOWN_FONT_SIZE
    
    # Calculate scale factor based on reference resolution (1440x900)
    SCALE_FACTOR = min(SCREEN_WIDTH / 1440, SCREEN_HEIGHT / 900)
    
    # Update UI dimensions
    UI_WIDTH = int(SCREEN_WIDTH * 0.15)
    GAME_WIDTH = int(SCREEN_WIDTH * 0.65)
    GAME_HEIGHT = int(SCREEN_HEIGHT * 0.75)
    
    # Update paddle settings
    PADDLE_WIDTH = int(200 * SCALE_FACTOR)
    PADDLE_HEIGHT = int(10 * SCALE_FACTOR)
    PADDLE_Y = int(SCREEN_HEIGHT - 70 * SCALE_FACTOR)
    
    # Update ball settings
    BALL_RADIUS = int(8 * SCALE_FACTOR)
    BALL_SPEED = int(5 * SCALE_FACTOR)
    
    # Update brick settings
    BRICK_WIDTH = int(54 * SCALE_FACTOR)
    BRICK_HEIGHT = int(20 * SCALE_FACTOR)
    BRICK_PADDING = int(8 * SCALE_FACTOR)
    
    # Update font sizes
    TITLE_FONT_SIZE = int(62 * SCALE_FACTOR)
    LABEL_FONT_SIZE = int(32 * SCALE_FACTOR)
    SCORE_FONT_SIZE = int(50 * SCALE_FACTOR)
    SMALL_FONT_SIZE = int(28 * SCALE_FACTOR)
    COUNTDOWN_FONT_SIZE = int(150 * SCALE_FACTOR)
