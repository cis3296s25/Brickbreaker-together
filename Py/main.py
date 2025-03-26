import pygame
from settings import *
from game import Game
from mainmenu import BrickBreakerMenu

def main():
    pygame.init()
    menu = BrickBreakerMenu()
    menu.run()

if __name__ == "__main__":
    main()