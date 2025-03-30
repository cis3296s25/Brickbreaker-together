import pygame
import random
from settings import *

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = random.choice(['bomb', 'multi_ball', 'extra_life', 'slow_ball'])
        self.speed = 3

        self.color_map = {
            'bomb': (231, 76, 60),        # Red
            'multi_ball': (52, 152, 219), # Blue
            'extra_life': (46, 204, 113), # Green
            'slow_ball': (241, 196, 15),  # Yellow
        }

        self.label_map = {
            'bomb': 'B',
            'multi_ball': 'M',
            'extra_life': '+',
            'slow_ball': 'S',
        }