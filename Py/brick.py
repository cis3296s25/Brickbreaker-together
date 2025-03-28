import pygame
import random
from settings import *

class Brick:
    def __init__(self, x, y, color=None):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color if color else BRICK_COLOR
        # light color and dark color in the brick
        self.light_color = self.get_lighter_color(self.color)
        self.dark_color = self.get_darker_color(self.color)

    def get_lighter_color(self, color):
        return tuple(min(c + 50, 255) for c in color)

    def get_darker_color(self, color):
        return tuple(max(c - 50, 0) for c in color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
        pygame.draw.line(screen, self.light_color, 
                        self.rect.topleft, self.rect.topright, 2)
        pygame.draw.line(screen, self.light_color, 
                        self.rect.topleft, self.rect.bottomleft, 2)
        
        pygame.draw.line(screen, self.dark_color, 
                        self.rect.bottomleft, self.rect.bottomright, 2)
        pygame.draw.line(screen, self.dark_color, 
                        self.rect.topright, self.rect.bottomright, 2)

