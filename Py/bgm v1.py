import pygame
from settings import *
from game import Game
from mainmenu import BrickBreakerMenu

def main():
    pygame.init()
    init_screen_dimensions()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("BrickBreaker Together")
    
    menu = BrickBreakerMenu(screen)
    menu.run()

if __name__ == "__main__":
    main()