import pygame
from settings import *
from game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BrickBreaker")
    game = Game(screen)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()