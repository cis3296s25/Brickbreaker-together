import pygame
from settings import *
from game import Game
from mainmenu import BrickBreakerMenu

def main():
    pygame.init()
    # Get the screen size
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("BrickBreaker Together")
    
    menu = BrickBreakerMenu(screen)
    menu.run()

if __name__ == "__main__":
    main()