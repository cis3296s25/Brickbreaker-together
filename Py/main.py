import pygame
from settings import *
from game import Game
from mainmenu import BrickBreakerMenu

def main():
    pygame.init()
    
    # Get the screen size
    info = pygame.display.Info()
    # THIS IS FOR BORDERLESS WINDOWED
    #screen = pygame.display.set_mode((1280, 720), pygame.SCALED | pygame.FULLSCREEN)
    # THIS IS FOR FULLSCREEN
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption("BrickBreaker Together")
    
    menu = BrickBreakerMenu(screen)
    menu.run()

if __name__ == "__main__":
    main()