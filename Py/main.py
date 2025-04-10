import pygame
import os
from settings import *
from game import Game
from mainmenu import BrickBreakerMenu

def center_window():
    """Center the game window on the screen"""
    os.environ['SDL_VIDEO_CENTERED'] = '1'

def main():
    pygame.init()
    # Initialize the mixer for sound
    pygame.mixer.init()
    init_screen_dimensions()
    
    # Center the window
    center_window()
    
    # Get the screen size and create a borderless window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME | pygame.FULLSCREEN)
    pygame.display.set_caption("BrickBreaker Together")
    
    menu = BrickBreakerMenu(screen)
    menu.run()

if __name__ == "__main__":
    main() 