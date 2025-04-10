import pygame
import os
import json
from settings import *
from game import Game
from mainmenu import BrickBreakerMenu

def center_window():
    """Center the game window on the screen"""
    os.environ['SDL_VIDEO_CENTERED'] = '1'

def load_user_settings():
    """Load user settings from the settings file"""
    settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_settings.json')
    default_settings = {
        'music_volume': 0.5,
        'sound_volume': 0.5,
        'screen_width': 1440,
        'screen_height': 900,
        'fullscreen': True
    }
    
    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                return json.load(f)
        return default_settings
    except Exception as e:
        print(f"Error loading settings: {e}")
        return default_settings

def main():
    pygame.init()
    # Initialize the mixer for sound
    pygame.mixer.init()
    
    # Load user settings
    user_settings = load_user_settings()
    
    # Update global screen dimensions with user settings
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = user_settings['screen_width']
    SCREEN_HEIGHT = user_settings['screen_height']
    
    init_screen_dimensions()
    
    # Center the window
    center_window()
    
    # Get the screen size and create window based on user settings
    if user_settings['fullscreen']:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME | pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.set_caption("BrickBreaker Together")
    
    menu = BrickBreakerMenu(screen)
    menu.run()

if __name__ == "__main__":
    main()